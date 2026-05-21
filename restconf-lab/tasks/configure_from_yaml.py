import yaml
import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

logging.basicConfig(
    filename='restconf_lab.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

HEADERS = {
    'Accept': 'application/vnd.yang.data+json',
    'Content-Type': 'application/vnd.yang.data+json'
}

def configure_interface(router, interface):
    host = router['host']
    username = router['username']
    password = router['password']

    interface_name = interface['name']
    encoded_interface = quote(interface_name, safe='')

    url = f"http://{host}/restconf/api/running/interfaces/interface/{encoded_interface}"

    payload = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": "Configured using RESTCONF and YAML",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": interface['ip'],
                        "netmask": interface['netmask']
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    try:
        logging.info(f"Configuring {router['name']} {interface_name} at {url}")

        response = requests.put(
            url,
            auth=HTTPBasicAuth(username, password),
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=10
        )

        if response.status_code in [200, 201, 204]:
            print(f"[SUCCESS] {router['name']} {interface_name} configured")
            logging.info(f"Success: {router['name']} {interface_name}")
        else:
            print(f"[FAILED] {router['name']} {interface_name} - Code {response.status_code}")
            print(response.text)
            logging.error(f"Failed: {router['name']} {interface_name} - {response.text}")

    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Could not connect to {router['name']} {host}")
        logging.error(f"Connection error for {router['name']}: {error}")

def main():
    with open('routers.yml', 'r') as file:
        data = yaml.safe_load(file)

    for router in data['routers']:
        for interface in router['interfaces']:
            configure_interface(router, interface)

if __name__ == "__main__":
    main()
