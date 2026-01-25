import os

import dotenv

from functions import create_page, get_pages, update_page

dotenv.load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API")
DATABASE_ID = os.getenv("database_id")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2025-09-03",
}

notion_details = {"DATABASE_ID": DATABASE_ID, "headers": headers}


pages = get_pages(notion_details=notion_details)
print("List of pages - ")
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    name = props["Name"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    created_date = props["Created Date"]["date"]["start"]
    status = props["Status"]["status"]["name"]
    print(name)
