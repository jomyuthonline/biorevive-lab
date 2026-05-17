import requests
import json
from PIL import Image

def add_watermark_and_repost():
    # 1. Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return

    # 2. Delete the post without watermark
    OLD_POST_ID = "122113127852744882"
    requests.delete(f"https://graph.facebook.com/v20.0/{OLD_POST_ID}?access_token={PAGE_TOKEN}")
    print(f"--- Deleted old post: {OLD_POST_ID} ---")

    # 3. Add Watermark to the image
    base_image_path = r"C:\Users\Bon8\.gemini\antigravity\brain\fda349bf-2d25-4b9b-b8f4-3055f721fb72\grease_trap_checklist_infographic_1778940998053.png"
    watermark_path = "assets/logo_transparent.png"
    output_path = "assets/infographic_watermarked.png"

    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")

        # Resize watermark (e.g., 15% of base image width)
        w_width = int(base_image.width * 0.15)
        w_height = int(watermark.height * (w_width / watermark.width))
        watermark = watermark.resize((w_width, w_height), Image.Resampling.LANCZOS)

        # Create a layer for the watermark
        transparent = Image.new('RGBA', base_image.size, (0,0,0,0))
        # Place at bottom right with some padding
        position = (base_image.width - w_width - 40, base_image.height - w_height - 40)
        transparent.paste(watermark, position)

        # Merge
        watermarked = Image.alpha_composite(base_image, transparent)
        watermarked.convert("RGB").save(output_path, "PNG")
        print("[OK] ใส่ลายน้ำสำเร็จแล้ว!")
    except Exception as e:
        print(f"[ERROR] Failed to add watermark: {e}")
        return

    # 4. Post the watermarked image
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

    with open(output_path, "rb") as f:
        files = {"source": f}
        data = {
            "message": caption,
            "access_token": PAGE_TOKEN
        }
        response = requests.post(post_url, files=files, data=data)
        
    result = response.json()
    if "id" in result:
        print(f"[OK] โพสต์พร้อมลายน้ำสำเร็จแล้ว!")
        print(f"ลิงก์โพสต์: https://www.facebook.com/{result['id']}")
    else:
        print("[ERROR] โพสต์ไม่สำเร็จ")
        print(result)

if __name__ == "__main__":
    add_watermark_and_repost()
