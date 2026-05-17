import requests
import json

def post_to_facebook():
    # Load credentials from the JSON file
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            # Use the first page found
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    caption = """BioRevive Lab - ฟื้นฟูน้ำเสียให้กลับมามีชีวิต 🌿✨

ยกระดับมาตรฐานความสะอาดให้ธุรกิจของคุณด้วย 'จุลินทรีย์เชื้อสด' Active 99%
✅ กำจัดกลิ่นเหม็นภายใน 24 ชม.
✅ สลายคราบไขมันถึงต้นตอ
✅ ปลอดภัยต่อคนและสัตว์เลี้ยง 100% (BCG Model)

พิเศษ! ชุดโปรโมชั่น Set S (ชุดทดลอง)
เพียง 611.- เท่านั้น (จากปกติ 679.-)
ในเซ็ตประกอบด้วย: แกลลอน 1L + ถุงชา 1 ถุง (6 ซอง)

สั่งซื้อหรือปรึกษาผู้เชี่ยวชาญฟรี:
Line: @biorevivelab
#BioReviveLab #จุลินทรีย์เชื้อสด #บำบัดน้ำเสีย #ร้านอาหาร #โรงแรม"""

    image_path = "assets/promo_set_s_lifestyle.png"
    
    print(f"--- Posting to Facebook Page: {PAGE_ID} ---")
    
    try:
        with open(image_path, "rb") as f:
            files = {
                "source": f
            }
            data = {
                "message": caption,
                "access_token": PAGE_TOKEN
            }
            response = requests.post(url, files=files, data=data)
            
        result = response.json()
        if "id" in result:
            print(f"[OK] โพสต์สำเร็จแล้ว!")
            print(f"ID โพสต์คือ: {result['id']}")
            print(f"สามารถดูโพสต์ได้ที่: https://www.facebook.com/{result['id']}")
        else:
            print("[ERROR] โพสต์ไม่สำเร็จ")
            print(result)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    post_to_facebook()
