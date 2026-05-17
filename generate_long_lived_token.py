import requests
import json

APP_ID = "1704404440762632"
APP_SECRET = "4618b0e11882694c277747f1cba6f1c0"
SHORT_TOKEN = "EAAYOJZAUZByQgBRZAEJae4ZBp0i2dzW1oSXK9gwqZCReyCrK76fWD6hKvvdrmeUX5qE6EfhJcweWZA3EH2IuBzhdhcfQsD91yVWTW0qaiPfdZAlSlOvDHfx51Ugqi71ZA97Q4bvdBo5ZBB49V0hXNGduSfJQaBn3KcxqTkZACtJmAfW07Yfd4JZCUxl8LeT8suQUlbQH4I01NFQDXIUwR73Fk8ocySSZAgIJLs4gI8AEMZAsSp8ZBd2ttOZCPv2tYb8aRZCObDJwjXzZBiGpQGXLHS4ZCbvfB1qfix"

def upgrade_token():
    print("--- Upgrading to Permanent Page Token ---")
    
    # 1. Exchange Short-lived Token for Long-lived User Token (lasts ~60 days)
    url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_TOKEN}"
    
    try:
        response = requests.get(url)
        data = response.json()
        long_user_token = data.get("access_token")
        
        if not long_user_token:
            print("[ERROR] Could not exchange for long-lived user token.")
            print(f"Details: {data}")
            return

        # 2. Get Page Tokens using the Long-lived User Token
        # Page tokens obtained this way for a developer who is an admin of the page NEVER expire.
        url_pages = f"https://graph.facebook.com/v20.0/me/accounts?access_token={long_user_token}"
        pages_res = requests.get(url_pages).json()
        
        if "data" in pages_res:
            print("[OK] Token Upgrade Successful! Saving permanent credentials...")
            with open("facebook_credentials.json", "w", encoding="utf-8") as f:
                json.dump(pages_res["data"], f, ensure_ascii=False, indent=4)
            
            for page in pages_res["data"]:
                print(f"- Page: {page['name']} (Permanent Token Active)")
            print("\n[INFO] You can now post anytime without refreshing tokens.")
        else:
            print("[ERROR] Failed to fetch page tokens.")
            print(pages_res)

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    upgrade_token()
