from netmiko import Netmiko

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

commands = [
    "interface Loopback100",
    "description Created using Netmiko",
    "ip address 100.100.100.100 255.255.255.255",
    "no shutdown"
]

net_connect = Netmiko(**device)
output = net_connect.send_config_set(commands)
print(output)
net_connect.disconnect()
