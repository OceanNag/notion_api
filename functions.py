import json
from typing import Any, Dict
import requests


def get_pages(notion_details: dict, num_pages=None):
    DATABASE_ID = notion_details["DATABASE_ID"]
    headers = notion_details["headers"]
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    response = requests.get(url, headers=headers)
    data = response.json()
    data_source_id = data["data_sources"][0]["id"]
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"

    payload = {"page_size": page_size}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    with open("db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {
            "page_size": page_size,
            "start_cursor": data["next_cursor"],
        }
        url = f"https://api.notion.com/v1/databases/{data_source_id}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def create_page(notion_details: dict, data: dict):
    DATABASE_ID = notion_details["DATABASE_ID"]
    headers = notion_details["headers"]
    create_url = "https://api.notion.com/v1/pages"

    name = data["name"]
    title = data["title"]
    created_date = data["created_date"]
    status = data["status"]

    post_data = {
        "Name": {"title": [{"text": {"content": name}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Created Date": {"date": {"start": created_date, "end": None}},
        "Status": {"status": {"name": status}},
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": post_data,
    }

    res = requests.post(create_url, headers=headers, json=payload)

    if res.status_code == 200:
        print(name, " - page created successfully")
    else:
        print(
            "error with posting page named", name, " - error", res.status_code
        )
    return res


def update_page(notion_details: dict, page_id: str, data: dict):
    headers = notion_details["headers"]
    url = f"https://api.notion.com/v1/pages/{page_id}"
    update_data: Dict[str, Any] = {}
    if "name" in data:
        update_data["Name"] = {"title": [{"text": {"content": data["name"]}}]}
    if "title" in data:
        update_data["Title"] = {
            "rich_text": [{"text": {"content": data["title"]}}]
        }
    if "created_date" in data:
        update_data["Created Date"] = {
            "date": {"start": data["created_date"], "end": None}
        }
    if "status" in data:
        update_data["Status"] = {"status": {"name": data["status"]}}

    payload = {"properties": update_data}
    res = requests.patch(url, json=payload, headers=headers)

    if res.status_code == 200:
        print(f"Page {page_id} updated successfully.")
    else:
        print(f"Error updating page {page_id}: {res.status_code}, {res.text}")
    return res
