import os
import dotenv
import functions

dotenv.load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API")
DATABASE_ID = os.getenv("database_id")

if NOTION_TOKEN is None:
    raise RuntimeError("NOTION_TOKEN is not set")
if DATABASE_ID is None:
    raise RuntimeError("DATABASE_ID is not set")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2025-09-03",
}

notion_details = {"DATABASE_ID": DATABASE_ID, "headers": headers}


pages = functions.get_pages(notion_details=notion_details)
print("List of pages - ")
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    name = props["Name"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    created_date = props["Created Date"]["date"]["start"]
    status = props["Status"]["status"]["name"]
    print(name)
