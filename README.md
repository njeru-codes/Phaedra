# PHEEDRA
This project provides a MITM ARP spoofing tool designed for capturing DNS traffic within a local network.

⚠️ Disclaimer: This tool is intended for educational and ethical use only. Unauthorized use on networks without explicit permission may violate legal and ethical standards.

## USAGE
clone repository
```
    git clone git@github.com:njeru-codes/Phaedra.git
    cd Phaedra
```
create a python virtual environment
```
    python3 -m venv venv
    source venv/bin/activate
```
install python dependecies
```python
    pip install -r requirements.txt
```
run the script
```bash
    #with venv environment
    sudo $(which python3) sniffer.py --network 0.0.0.0/24 --iface eth0 --router_ip 0.0.0.1

    #without venv
    sudo sniffer.py --network 0.0.0.0/24 --iface eth0 --router_ip 0.0.0.1
```

## SCREENSHOTS

![Screenshot From 2024-12-22 03-13-26](https://github.com/user-attachments/assets/5e42b704-2b2c-46c4-b5fe-02c0d7d8782b)
