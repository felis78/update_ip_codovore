from typing import Optional, Dict, Any

import requests
import json
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='fix_ip.log',
    encoding='utf-8',
    level=logging.DEBUG
)
logger = logging.getLogger("fix_ip")

def get_registered_ip(zone_id: int, bearer_token: str, domain_name: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = f"https://api.infomaniak.com/2/zones/{domain_name}/records"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        records = response.json().get('data', [])
        
        for record in records:
            if record['id'] == zone_id:
                return record['target']
    
    except requests.RequestException as e:
        logger.critical(f'Error fetching registered IP: {e}')
    
    return None

def get_public_ip(url_ipfy: str = 'https://api.ipify.org?format=json') -> Optional[str]:
    try:
        response = requests.get(url_ipfy)
        response.raise_for_status()
        return response.json().get('ip')
    
    except requests.RequestException as e:
        logger.critical(f'Error getting public IP: {e}')
    
    return None

def update_dns_record(zone_id: int, domain_name: str, new_ip: str, bearer_token: str) -> Optional[Dict[str, Any]]:
    url = f"https://api.infomaniak.com/2/zones/{domain_name}/records/{zone_id}"
    headers = {
        'Authorization': f"Bearer {bearer_token}",
        'Content-Type': 'application/json',
    }
    data = json.dumps({"target": new_ip})
    
    try:
        response = requests.put(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        logger.critical(f"Error updating DNS record: {e}")
    
    return None

def synchronize_dns_ip(zone_id: int, bearer_token: str, domain_name: str) -> None:
    registered_ip = get_registered_ip(zone_id, bearer_token, domain_name)
    public_ip = get_public_ip()
    
    if not registered_ip or not public_ip:
        logger.error("Failed to retrieve IP addresses.")
        return
    
    if public_ip != registered_ip:
        logger.info(f'IP mismatch detected: current IP {public_ip}, registered IP {registered_ip}. Updating record.')
        result = update_dns_record(zone_id, domain_name, public_ip, bearer_token)
        
        if result:
            logger.info(f'IP updated successfully to {public_ip}')
        else:
            logger.error('Failed to update IP.')
    else:
        logger.info("IP is up to date, no change needed.")


if __name__ == "__main__":
    ZONE_ID: int = < Number: id de la zone dns à modifier >
    BEARER_TOKEN: str = "< String: clé api >"
    DOMAIN_NAME: str = "< String: nom de domaine cible >"
    
    synchronize_dns_ip(ZONE_ID, BEARER_TOKEN, DOMAIN_NAME)
