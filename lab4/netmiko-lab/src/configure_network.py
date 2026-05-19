import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

logging.basicConfig(
    filename="network_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

with open("network.yml") as file:
    data = yaml.load(file, Loader=yaml.SafeLoader)

env = Environment(
    loader=FileSystemLoader("."),
    trim_blocks=True,
    lstrip_blocks=True
)

template = env.get_template("router_config.j2")

for router in data["routers"]:
    device = {
        "device_type": router["device_type"],
        "ip": router["mgmt_ip"],
        "username": router["username"],
        "password": router["password"],
        "port": 22,
    }

    try:
        logging.info(f"Connecting to {router['hostname']} at {router['mgmt_ip']}")
        net_connect = Netmiko(**device)

        config_output = template.render(router=router)
        commands = config_output.splitlines()

        output = net_connect.send_config_set(commands)
        print(f"\n===== Configuration pushed to {router['hostname']} =====")
        print(output)

        logging.info(f"Successfully configured {router['hostname']}")
        net_connect.disconnect()

    except Exception as error:
        print(f"Error configuring {router['hostname']}: {error}")
        logging.error(f"Failed to configure {router['hostname']}: {error}")
