import requests
import json

def delete_and_repost():
    # 1. Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    # 2. Delete the old post
    OLD_POST_ID = "122113120082744882"
    delete_url = f"https://graph.facebook.com/v20.0/{OLD_POST_ID}?access_token={PAGE_TOKEN}"
    
    print(f"--- Deleting old post: {OLD_POST_ID} ---")
    del_res = requests.delete(delete_url).json()
    if del_res.get("success"):
        print("[OK] ลบโพสต์เก่าเรียบร้อยแล้ว!")
    else:
        print(f"[WARNING] ไม่สามารถลบโพสต์ได้ (อาจถูกลบไปแล้ว): {del_res}")

    # 3. Post the new one WITHOUT PRICE
    post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    caption = """BioRevive Lab - ฟื้นฟูน้ำเสียให้กลับมามีชีวิต 🌿✨

ยกระดับมาตรฐานความสะอาดให้ธุรกิจของคุณด้วย 'จุลินทรีย์เชื้อสด' Active 99%
✅ กำจัดกลิ่นเหม็นภายใน 24 ชม.
✅ สลายคราบไขมันถึงต้นตอ
✅ ปลอดภัยต่อคนและสัตว์เลี้ยง 100% (BCG Model)

พิเศษ! ชุดโปรโมชั่น Set S (ชุดทดลอง) สำหรับธุรกิจเริ่มต้น
ในเซ็ตประกอบด้วย: แกลลอน 1L + ถุงชา 1 ถุง (6 ซอง)

🌐 รายละเอียดเพิ่มเติมและประเมินความเสี่ยงฟรี: 
https://biorevive-lab.vercel.app/

สอบถามข้อมูลเพิ่มเติมหรือขอรับคำปรึกษาจากผู้เชี่ยวชาญ:
Line: @biorevivelab
Inbox: m.me/biorevivelab

#BioReviveLab #จุลินทรีย์เชื้อสด #บำบัดน้ำเสีย #ร้านอาหาร #โรงแรม"""

    image_path = "assets/promo_set_s_lifestyle.png"
    
    print(f"--- Reposting to Facebook Page: {PAGE_ID} ---")
    
    with open(image_path, "rb") as f:
        files = {"source": f}
        data = {
            "message": caption,
            "access_token": PAGE_TOKEN
        }
        response = requests.post(post_url, files=files, data=data)
        
    result = response.json()
    if "id" in result:
        print(f"[OK] โพสต์ใหม่สำเร็จแล้ว (ไม่มีราคา 100%)")
        print(f"ลิงก์โพสต์ใหม่: https://www.facebook.com/{result['id']}")
    else:
        print("[ERROR] โพสต์ไม่สำเร็จ")
        print(result)

if __name__ == "__main__":
    delete_and_repost()
