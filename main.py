import requests
import json
import logging

logger = logging.getLogger("fix_ip")
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', filename='fix_ip.log', encoding='utf-8',
                    level=logging.DEBUG)
url_ipfy = 'https://api.ipify.org?format=json'
zoneId = < Number: id de la zone dns à modifier >
bearer_token = "<String: clé api >"
domainName = "< String: nom de domaine cible >"


def get_registred_ip():
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = "https://api.infomaniak.com/2/zones/codovore.fr/records"
    try:
        response = requests.get(url, headers=headers)
        datas = response.json()
        for i in datas['data']:
            if i['id'] == zoneId:
                return i['target']

    except requests.exceptions.RequestException as e:
        logging.critical(f'Error: {e}')
        return False


def get_public_ip():
    try:
        response = requests.get(url_ipfy)
        response.raise_for_status()
        return response.json()['ip']

    except requests.exceptions.RequestException as e:
        logging.critical(f'Error getting public IP: {e}')
        return False


def fixBadIp(newIp):
    url_put = f"https://api.infomaniak.com/2/zones/{domainName}/records/{zoneId}"
    headers = {
        'Authorization': f"Bearer {bearer_token}",
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "target": newIp,
    })
    try:
        req = requests.request("PUT", url=url_put, data=data, headers=headers)
        res = req.json()

    except requests.exceptions.RequestException as e:
        logger.critical(f"Error: {e}")
        return False
    return res


infomaniakIp = get_registred_ip()
actualIp = get_public_ip()

if infomaniakIp is False or actualIp is False:
    exit()

if actualIp != infomaniakIp:
    logging.info(f'Ip has changed: actual IP{actualIp} - registred ip: {infomaniakIp}. Trying to fix it.')
    try:
        fixBadIp(actualIp)

    except Exception as e:
        print(e)

    else:
        logging.info(f'Ip updated. New ip: {actualIp}\n')

else:
    logging.info("IP is un to date, nothing to change \n")
