import requests
from downerhelper.secrets import get_key_url
import base64

def get_sharepoint_list(site_address, list_name, curr_id, keyvault_url, queue) -> dict:
    try:
        key_url = get_key_url('get-sharepoint-list', keyvault_url, queue)
    except Exception as e:
        queue.add('ERROR', f"Error getting key/URL for SharePoint list {list_name} at {site_address}: {e}")
        raise e

    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "curr_id": curr_id
            }
        )
        if not response.ok: raise Exception('Failed to get data from SharePoint list')
        return response.json()['value']
    except Exception as e:
        queue.add('ERROR', f"Error getting SharePoint list {list_name} at {site_address}: {e}")
        raise e
    
def form_sharepoint_list_item(attributes, title, pairs, queue):
    try:
        item = {}
        for key, value in pairs.items():
            try:
                if value is None:
                    item[key] = ''
                    continue
                if isinstance(value, list):
                    values = []
                    for val in value:
                        if val is None: continue
                        if val not in attributes.keys(): continue
                        if attributes[val] in [None, '']: continue
                        values.append(attributes[val])
                    item[key] = ' '.join(values)
                    continue
                item[key] = attributes[value]
            except KeyError:
                item[key] = ''
        item['Title'] = title
        return item
    except Exception as e:
        queue.add('ERROR', f"Error forming SharePoint list item: {e}")
        raise e

def create_sharepoint_list_item(item, site_address, list_name, key_url, queue):
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item": item
            }
        ) 
        if not response.ok: raise Exception('Failed to create item in SharePoint list')
        return response.json()['id']
    except Exception as e:
        queue.add('ERROR', f"Error creating SharePoint list item on {list_name} at {site_address}: {e}")
        raise e
    
def create_sharepoint_list_attachment(item_id, attachment, attachment_name, site_address, list_name, key_url, queue) -> bool:   
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item_id": item_id,
                "attachment": base64.b64encode(attachment).decode('utf-8'),
                "attachment_name": attachment_name
            },
            headers={
                'Content-Type': 'application/json'
            }
        ) 
        if not response.ok: raise Exception('Failed to create item in SharePoint list')
        return True
    
    except Exception as e:
        queue.add('ERROR', f"Error creating SharePoint list attachment on item {item_id} in {list_name} at {site_address}: {e}")
        raise e
    
def get_sharepoint_list_attachments(item_id, site_address, list_name, key_url, queue) -> list:   
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item_id": item_id
            }
        )
        if not response.ok: raise Exception('Failed to get data from SharePoint list')
        return response.json()
    except Exception as e:
        queue.add('ERROR', f"Error getting SharePoint list attachments: {e}")
        return []