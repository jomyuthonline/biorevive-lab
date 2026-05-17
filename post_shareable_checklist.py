import requests
import json

def post_shareable_checklist():
    # 1. Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    # 2. Post Shareable Infographic
    post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    caption = """[SAVE ไว้ให้พนักงานดู!] คู่มือ 5 ขั้นตอน ดูแลถังดักไขมันให้ไร้กลิ่นเหม็นตลอดกาล 🛠️กริบเหมือนวันแรกที่เปิดร้าน

ปัญหากลิ่นเหม็นจากครัว ไม่ใช่เรื่องเล่นๆ ครับ เพราะมันส่งผลต่อความรู้สึกของลูกค้าและสุขอนามัยในร้าน วันนี้ BioRevive Lab สรุป Checklist ง่ายๆ ที่จะช่วยให้ระบบบำบัดของคุณทำงานได้ 100% มาให้แล้วครับ:

1️⃣ ตักไขมันหนาหน้าบ่อออกทุกเช้า: อย่าปล่อยให้เป็นแผ่นแข็ง เพราะจะทำให้จุลินทรีย์ทำงานยากขึ้น
2️⃣ งดใช้โซดาไฟหรือสารเคมีรุนแรง: สารเหล่านี้จะฆ่าจุลินทรีย์ธรรมชาติ และทำให้ไขมันจับตัวเป็นก้อนแข็งในท่อ
3️⃣ ตรวจสอบระดับน้ำ: ถังดักไขมันต้องมีน้ำอยู่ในระดับที่เหมาะสมเสมอเพื่อให้เกิดการแยกชั้นไขมันที่ถูกต้อง
4️⃣ เติมจุลินทรีย์เชื้อสดสม่ำเสมอ: เพื่อช่วยย่อยสลายไขมันส่วนเกินที่ล้างออกไม่หมด และกำจัดกลิ่นสะสม
5️⃣ ทำความสะอาดตะแกรงดักเศษอาหารทุกวัน: ป้องกันการเน่าเสียของเศษอาหารที่ตกค้าง

✅ แชร์โพสต์นี้เก็บไว้ในกลุ่มพนักงาน หรือส่งต่อให้เพื่อนร่วมอาชีพได้เลยครับ!

🌐 หากต้องการตรวจสอบจุดเสี่ยงอื่นๆ เพิ่มเติม เข้าไปใช้เครื่องมือ Checklist ของเราได้ที่:
https://biorevivelab.vercel.app/checklist.html

#BioReviveLab #คู่มือร้านอาหาร #ถังดักไขมัน #สุขอนามัยในครัว #SMEร้านอาหาร"""

    # Using the generated infographic image
    image_path = r"C:\Users\Bon8\.gemini\antigravity\brain\fda349bf-2d25-4b9b-b8f4-3055f721fb72\grease_trap_checklist_infographic_1778940998053.png"
    
    print(f"--- Posting SHAREABLE CHECKLIST to Facebook Page: {PAGE_ID} ---")
    
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
            print(f"[OK] โพสต์คู่มือสำเร็จแล้ว!")
            print(f"ลิงก์โพสต์: https://www.facebook.com/{result['id']}")
        else:
            print("[ERROR] โพสต์ไม่สำเร็จ")
            print(result)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    post_shareable_checklist()
