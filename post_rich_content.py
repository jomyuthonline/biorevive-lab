import requests
import json

def repost_with_content():
    # 1. Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    # 2. Delete the salesy post
    SALES_POST_ID = "122113124582744882"
    delete_url = f"https://graph.facebook.com/v20.0/{SALES_POST_ID}?access_token={PAGE_TOKEN}"
    
    print(f"--- Deleting sales post: {SALES_POST_ID} ---")
    requests.delete(delete_url)

    # 3. Post the CONTENT-FOCUSED one
    post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    caption = """ทำไมถังดักไขมันยังมีกลิ่นเหม็น? ทั้งที่เพิ่งจ้างรถมาดูดไปไม่นาน... 🤢🚫

เจ้าของร้านอาหารและโรงแรมหลายท่านอาจเคยเจอปัญหานี้ครับ ต้นตอจริงๆ ไม่ได้อยู่ที่ปริมาณของเสียเท่านั้น แต่อยู่ที่ "คราบไขมันสะสม" ที่เกาะแน่นตามผนังท่อและบ่อบัก ซึ่งรถดูดออกได้ไม่หมด

BioRevive Lab ขอนำเสนอ "จุลินทรีย์เชื้อสด" นวัตกรรมที่เกิดจากประสบการณ์กว่า 20 ปี ในการดูแลระบบนิเวศ
✅ ย่อยสลายไขมันถึงระดับโมเลกุล: เปลี่ยนไขมันให้เป็นน้ำและก๊าซคาร์บอนไดออกไซด์
✅ กำจัดกลิ่นที่ต้นเหตุ: ไม่ใช่การใช้กลิ่นน้ำหอมมากลบ แต่เป็นการกำจัดแบคทีเรียที่ทำให้เกิดกลิ่น
✅ ปลอดภัยและยั่งยืน: มาตรฐาน BCG Model เป็นมิตรต่อพนักงานและสิ่งแวดล้อม 100%

เปลี่ยนร้านของคุณให้สะอาด สดชื่น และได้มาตรฐานสุขอนามัยที่ดีที่สุด เพื่อรอยยิ้มของลูกค้าในทุกวันครับ

🌐 ศึกษาข้อมูลเพิ่มเติมและประเมินความเสี่ยงฟรี: 
https://biorevivelab.vercel.app/

สอบถามหรือขอรับคำปรึกษาจากผู้เชี่ยวชาญ:
Line: @biorevivelab
#BioReviveLab #จุลินทรีย์เชื้อสด #บำบัดน้ำเสีย #ความรู้ร้านอาหาร #SMEไทย"""

    image_path = "assets/promo_set_s_lifestyle.png"
    
    print(f"--- Posting CONTENT to Facebook Page: {PAGE_ID} ---")
    
    with open(image_path, "rb") as f:
        files = {"source": f}
        data = {
            "message": caption,
            "access_token": PAGE_TOKEN
        }
        response = requests.post(post_url, files=files, data=data)
        
    result = response.json()
    if "id" in result:
        print(f"[OK] โพสต์คอนเทนต์สำเร็จแล้ว!")
        print(f"ลิงก์โพสต์: https://www.facebook.com/{result['id']}")
    else:
        print("[ERROR] โพสต์ไม่สำเร็จ")
        print(result)

if __name__ == "__main__":
    repost_with_content()
