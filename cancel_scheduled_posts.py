import requests
import json

def delete_post(post_id):
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    url = f"https://graph.facebook.com/v20.0/{post_id}?access_token={PAGE_TOKEN}"
    response = requests.delete(url)
    result = response.json()
    if result.get("success"):
        print(f"[OK] Post {post_id} deleted successfully.")
    else:
        print(f"[ERROR] Failed to delete post {post_id}: {result}")

if __name__ == "__main__":
    post_ids = ["122113249898744882", "122113249994744882", "122113250042744882"]
    for pid in post_ids:
        delete_post(pid)
