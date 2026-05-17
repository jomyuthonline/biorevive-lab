import requests

TOKEN = "EAAYOJZAUZByQgBRZAEJae4ZBp0i2dzW1oSXK9gwqZCReyCrK76fWD6hKvvdrmeUX5qE6EfhJcweWZA3EH2IuBzhdhcfQsD91yVWTW0qaiPfdZAlSlOvDHfx51Ugqi71ZA97Q4bvdBo5ZBB49V0hXNGduSfJQaBn3KcxqTkZACtJmAfW07Yfd4JZCUxl8LeT8suQUlbQH4I01NFQDXIUwR73Fk8ocySSZAgIJLs4gI8AEMZAsSp8ZBd2ttOZCPv2tYb8aRZCObDJwjXzZBiGpQGXLHS4ZCbvfB1qfix"

def check_pages():
    print("--- Starting Facebook Connection Check ---")
    # Note: Use v20.0 or the latest stable version
    url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={TOKEN}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if "data" in data:
            if len(data["data"]) == 0:
                print("[ERROR] Connected, but NO pages found. Please ensure you selected the Page in the login popup.")
            else:
                print(f"[OK] Connected successfully! Found {len(data['data'])} pages:")
                import json
                with open("facebook_credentials.json", "w", encoding="utf-8") as f:
                    json.dump(data["data"], f, ensure_ascii=False, indent=4)
                for page in data["data"]:
                    print(f"\n- Page Name: {page['name']}")
                    print(f"  Page ID: {page['id']}")
                    print(f"  Page Token: {page['access_token']}")
                print("\n[INFO] Full credentials saved to facebook_credentials.json")
        else:
            print("[ERROR] Connection failed or Token is invalid.")
            print(f"Error Details: {data}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")

if __name__ == "__main__":
    check_pages()
