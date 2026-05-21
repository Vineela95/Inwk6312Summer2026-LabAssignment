import logging
import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)

HOST = '192.168.1.101'
USER = 'student'
PASSWORD = 'Meilab123'

BASE_URL = f'http://{HOST}/restconf/api/running/'

def set_interface(interface_name, ip_address, netmask):
    encoded_interface = quote(interface_name, safe='')
    url = BASE_URL + f'interfaces/interface/{encoded_interface}'

    auth = HTTPBasicAuth(USER, PASSWORD)

    headers = {
        'Accept': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }

    data = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": "Changed through RESTCONF",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip_address,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    logging.info(f"URL ==> {url}")

    response = requests.put(
        url,
        auth=auth,
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code in [200, 201, 204]:
        logging.info(f"Request successful on {HOST}, Code: {response.status_code}")
        return "success!"
    else:
        logging.error(f"Error on {HOST}, Code: {response.status_code}")
        return response.text

print(set_interface("GigabitEthernet3", "10.0.10.3", "255.255.255.0"))
