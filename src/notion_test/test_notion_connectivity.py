import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_SUB_DB_ID = os.getenv("NOTION_SUB_DB_ID")

# Notion APIのエンドポイント
url = "https://api.notion.com/v1/pages"

# 通信の身分証明（ヘッダー）
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 完璧に型合わせが完了したデータ（ペイロード）
payload = {
    "parent": {"database_id": NOTION_SUB_DB_ID},
    "properties": {
        "Name": {
            "title": [{"text": {"content": "Test - 10分デリバリー通信テスト"}}]
        },
        "Video ID": {
            "rich_text": [{"text": {"content": "dQw4w9WgXcQ"}}]
        },
        "Status": {
            "status": {"name": "Ready"}
        }
    }
}

print("🚀 KIOXIA SSDの隔離空間より通信を開始します...")

# NotionへデータをPush
response = requests.post(url, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
print(response.text)
