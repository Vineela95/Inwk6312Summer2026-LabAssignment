import logging
import requests
from requests.auth import HTTPBasicAuth
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)

HOST = '192.168.1.101'
USER = 'student'
PASSWORD = 'Meilab123'

BASE_URL = f'http://{HOST}/restconf/api/running/'

def get_interfaces(append_url):
    url = BASE_URL + append_url
    auth = HTTPBasicAuth(USER, PASSWORD)
    headers = {
        'Accept': 'application/vnd.yang.data+json'
    }

    logging.info(f"URL ==> {url}")

    response = requests.get(url, auth=auth, headers=headers)

    if response.status_code == 200:
        logging.info(f"Request successful on {HOST}, Code: {response.status_code}")
        return json.dumps(response.json(), sort_keys=True, indent=4)
    else:
        logging.error(f"Error on {HOST}, Code: {response.status_code}")
        return response.text

print(get_interfaces('interfaces'))
