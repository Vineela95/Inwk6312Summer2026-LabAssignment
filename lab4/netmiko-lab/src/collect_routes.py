import yaml
import logging
from netmiko import Netmiko

logging.basicConfig(
    filename="route_collection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

with open("network.yml") as file:
    data = yaml.load(file, Loader=yaml.SafeLoader)

for router in data["routers"]:
    device = {
        "device_type": router["device_type"],
        "ip": router["mgmt_ip"],
        "username": router["username"],
        "password": router["password"],
        "port": 22,
    }

    try:
        logging.info(f"Connecting to {router['hostname']} for route collection")
        net_connect = Netmiko(**device)

        routes = net_connect.send_command("show ip route", use_textfsm=True)

        print(f"\n===== Routing Table for {router['hostname']} =====")

        if isinstance(routes, list):
            for route in routes:
                print(
                    f"Protocol: {route.get('protocol')} | "
                    f"Network: {route.get('network')} | "
                    f"Distance: {route.get('distance')} | "
                    f"Metric: {route.get('metric')}"
                )
        else:
            print(routes)

        logging.info(f"Successfully collected routes from {router['hostname']}")
        net_connect.disconnect()

    except Exception as error:
        print(f"Error collecting routes from {router['hostname']}: {error}")
        logging.error(f"Failed to collect routes from {router['hostname']}: {error}")
