import os, requests
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv('NOTION_API_KEY')

DB_URL = "https://api.notion.com/v1/databases"
PAGE_URL = "https://api.notion.com/v1/pages"
BLOCK_URL = 'https://api.notion.com/v1/blocks'

HTTP_HEADERS = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'}

def create_page(db_id: str, props: dict, icon: dict = None):
    headers = HTTP_HEADERS
    body = {'parent': {'database_id': db_id}, 'properties': props}
    if icon: body['icon'] = icon
    r = requests.post(PAGE_URL, headers=headers, json=body)
    print(f'CREATE [{r.status_code}]')
    response_content = r.json()
    if r.status_code != 200: print(response_content)
    return response_content

def get_pages(database: str, limit: int = None, sorts: list = None, filter: dict = None):
    headers = HTTP_HEADERS
    payload = {}
    if limit: payload['page_size'] = limit
    if filter: payload['filter'] = filter
    if sorts: payload['sorts'] = sorts
    r = requests.post(DB_URL + f'/{database}' + '/query', json=payload, headers=headers)
    response_content = r.json()
    if r.status_code != 200: print(response_content)
    return response_content

def update_page(page_id: str, props: dict, archive: bool = False, icon: dict = None):
    headers = HTTP_HEADERS
    body = {'properties': props}
    if icon: body['icon'] = icon
    if archive: body.update({'archived': archive})
    r = requests.patch(PAGE_URL + f'/{page_id}', headers=headers, json=body)
    print(f'[UPDATE: {r.status_code}]')
    if r.status_code != 200: print(r.content)
    return r.status_code == 200

def get_text(property: dict):
    return (property['rich_text'][0]['plain_text']
            if 'plain_text' in property['rich_text'][0]
            else property['rich_text'][0]['text']['content'])

def to_title(s: str): return {'title': [{'text': {'content': s}}]}
def to_relation(id: str): return {'relation': [{'id': id}]}