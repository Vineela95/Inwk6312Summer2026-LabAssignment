from netmiko import ConnectHandler

devices = [
    {"device_type": "cisco_ios", "ip": "192.168.1.101", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.102", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.103", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.104", "username": "student", "password": "Meilab123", "port": "22"},
]

for device in devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show interface description")
    net_connect.disconnect()

    print("-" * 80)
    print(device["ip"])
    print(output)
