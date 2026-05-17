import requests
import json

def post_human_content():
    # 1. Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    # 2. Post content with Human element
    post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    caption = """เบื้องหลังความหอมสะอาดของอาคารระดับพรีเมียม... ไม่ใช่แค่การล้าง แต่คือการ 'เติม' จุลินทรีย์ครับ 🌿✨

หลายคนสงสัยว่า ทำไมโรงแรมหรือร้านอาหารระดับท็อป ถึงจัดการเรื่องกลิ่นเหม็นจากท่อระบายน้ำได้กริบขนาดนี้? 
คำตอบอยู่ในซองเล็กๆ นี้ครับ 'BioRevive Microbial Sachet' หรือจุลินทรีย์แบบถุงชาที่เราตั้งใจพัฒนามาเพื่อความสะดวกและประสิทธิภาพสูงสุด

✅ ใช้งานง่ายที่สุด: เพียงหย่อนลงในจุดที่มีกลิ่น (อ่างล้างหน้า, ท่อระบายน้ำ, โถสุขภัณฑ์)
✅ ทำงานต่อเนื่อง 24 ชม.: จุลินทรีย์จะค่อยๆ แตกตัวและย่อยสลายของเสียสะสมที่ต้นเหตุ
✅ ปลอดภัย 100%: ไม่มีสารเคมีกัดกร่อนท่อ ไม่เป็นอันตรายต่อพนักงานและแขกผู้เข้าพัก

เปลี่ยนการทำความสะอาดแบบเดิมๆ ที่ยุ่งยาก ให้เป็นเรื่องง่ายและยั่งยืนตามมาตรฐาน BCG Model ครับ

🌐 เช็คจุดเสี่ยงในอาคารของคุณได้ที่ Hygiene Checklist: 
https://biorevivelab.vercel.app/checklist.html

สอบถามข้อมูลหรือขอรับคำปรึกษาจากผู้เชี่ยวชาญ:
Line: @biorevivelab
#BioReviveLab #SustainableCleaning #LuxuryHotel #MicrobialSachet #จุลินทรีย์ถุงชา"""

    # Image provided by user (I'll assume it's saved as assets/user_post_image.jpg)
    image_path = "assets/user_post_image.jpg"
    
    print(f"--- Posting HUMAN content to Facebook Page: {PAGE_ID} ---")
    
    try:
        with open(image_path, "rb") as f:
            files = {"source": f}
            data = {
                "message": caption,
                "access_token": PAGE_TOKEN
            }
            response = requests.post(post_url, files=files, data=data)
            
        result = response.json()
        if "id" in result:
            print(f"[OK] โพสต์สำเร็จแล้ว!")
            print(f"ลิงก์โพสต์: https://www.facebook.com/{result['id']}")
        else:
            print("[ERROR] โพสต์ไม่สำเร็จ")
            print(result)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    post_human_content()
