import requests
import json
import time
from datetime import datetime

def schedule_post(image_path, caption, timestamp):
    # Load credentials
    try:
        with open("facebook_credentials.json", "r", encoding="utf-8") as f:
            credentials = json.load(f)
            PAGE_ID = credentials[0]["id"]
            PAGE_TOKEN = credentials[0]["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return False

    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    print(f"--- Scheduling Post for {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    try:
        with open(image_path, "rb") as f:
            files = {
                "source": f
            }
            data = {
                "message": caption,
                "published": "false",
                "scheduled_publish_time": str(int(timestamp)),
                "access_token": PAGE_TOKEN
            }
            response = requests.post(url, files=files, data=data)
            
        result = response.json()
        if "id" in result:
            print(f"[OK] Scheduled successfully!")
            print(f"Post ID: {result['id']}\n")
            return True
        else:
            print("[ERROR] Failed to schedule post")
            print(result)
            return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # REDESIGNED CAPTIONS: Exactly ONE matching link per post, no other links. Pure educational, tie-in style.
    
    ep1_caption = """🚨 ภัยเงียบใต้ซิงค์! ทำไมทำความสะอาดครัวทุกวัน แต่ยังมี "กลิ่นเหม็นตีกลับ" รบกวน?

หลายร้านอาหารหรือคาเฟ่ดูแลความสะอาดเคาน์เตอร์และพื้นผิวอย่างดีเยี่ยม แต่กลับตกม้าตายเรื่อง "กลิ่นสะสม" 
รู้หรือไม่ครับว่า... คราบไขมันจากนม เนย หรือน้ำมันทำอาหารที่เราล้างลงท่อไป ไม่ได้ไหลหายไปทั้งหมด แต่มันจะค่อยๆ เกาะจับตัวเป็นแผ่นหนาอยู่ตามผนังท่อน้ำทิ้ง!

เมื่อเวลาผ่านไป คราบไขมันเหล่านี้จะเน่าหมักหมม แบคทีเรียร้ายจะสร้างก๊าซไฮโดรเจนซัลไฟด์ (ก๊าซไข่เน่า) ส่งกลิ่นย้อนขึ้นมาตามท่อระบายน้ำรบกวนลูกค้าในร้าน ☕✨

การใช้สารเคมีรุนแรงราดลงท่ออาจเป็นวิธีแก้ไขชั่วคราว แต่ฤทธิ์กัดกร่อนจะทำให้ข้อต่อท่อชำรุดเสียหายในระยะยาว และไม่สามารถแก้ปัญหาย่อยสลายคราบอินทรีย์ฝังลึกได้จริง
แนวทางที่ยั่งยืนคือการบำบัดทางชีวภาพ โดยใช้ "จุลินทรีย์ธรรมชาติสายพันธุ์ย่อยสลายไขมัน" เข้าไปทำความสะอาดผนังท่อจากภายในอย่างปลอดภัย

ร่วมสร้างบรรยากาศร้านที่สมบูรณ์แบบด้วยแนวคิดความยั่งยืนกับ BioRevive Lab

🔍 ประเมิน 5 จุดเสี่ยงระบบน้ำทิ้งในร้านของคุณฟรี:
👉 https://biorevive-lab.vercel.app/checklist.html

💬 ปรึกษาปัญหาระบบกลิ่น LINE OA: @biorevivelab
#ดับกลิ่นท่อ #คาเฟ่ #สุขอนามัยในครัว #สุขาภิบาลร้านอาหาร #BioReviveLab"""

    ep2_caption = """🪤 ถังดักไขมัน... ดักไว้ได้จริง หรือกลายเป็นแค่ "แหล่งสะสมเชื้อโรค" ในร้านอาหาร?

"ถังดักไขมัน" คือด่านแรกที่ช่วยปกป้องระบบระบายน้ำสาธารณะ แต่ผู้ประกอบการหลายท่านอาจลืมไปว่า ถังดักไขมันทำหน้าที่เพียงแค่ "กักเก็บ" เท่านั้น หากไม่มีกระบวนการ "ย่อยสลาย" ถังดักจะกลายเป็นบ่อหมักหมมไขมันเน่าบูดขนาดใหญ่ทันที 🤢

ผลเสียที่ตามมาส่งผลกระทบต่อภาพลักษณ์แบรนด์โดยตรง:
🦟 เป็นแหล่งดึงดูดหนู แมลงสาบ และแมลงวันเข้ามาในพื้นที่เตรียมอาหาร
💨 กลิ่นเหม็นรบกวนลูกค้าในร้านทำลายบรรยากาศการทานอาหาร
💸 เกิดปัญหาท่อหลักอุดตันจนน้ำเอ่อล้น ทำให้ต้องเสียค่าลอกท่ออยู่บ่อยครั้ง

ทางออกที่เป็นมิตรต่อสิ่งแวดล้อมและคุ้มค่าที่สุดคือ การสร้าง "ระบบนิเวศบำบัดตัวเอง" ภายในถังดัก
ด้วยการเติมจุลินทรีย์ธรรมชาติที่มีความแอคทีฟสูง เข้าไปย่อยไขมันหนาเตอะให้กลายเป็นน้ำและก๊าซคาร์บอนไดออกไซด์อย่างเป็นธรรมชาติ ช่วยลดความถี่ในการตักทิ้งและล้างถังได้อย่างมหาศาล

เสริมสร้างสุขอนามัยร้านอาหารยุคใหม่ด้วยระบบชีวภาพบำบัด BioRevive Lab

📂 ดาวน์โหลดสไลด์แนวทางการบริหารจัดการระบบน้ำทิ้งร้านอาหาร:
👉 https://biorevive-lab.vercel.app/pitch_deck.html

💬 ปรึกษาปัญหาระบบกลิ่น LINE OA: @biorevivelab
#ถังดักไขมัน #สุขอนามัยร้านอาหาร #ระบบระบายน้ำ #จัดการร้านอาหาร #BioReviveLab"""

    ep3_caption = """🏨 มาตรฐานน้ำทิ้ง (BOD/COD) เรื่องใหญ่ของธุรกิจโรงแรมระดับพรีเมียมที่มองข้ามไม่ได้!

ในอุตสาหกรรมโรงแรมและการบริการ การควบคุมคุณภาพน้ำทิ้งจากอาคารก่อนปล่อยสู่ธรรมชาติมีกฎหมายและข้อบังคับที่เข้มงวดมาก หากค่า BOD (ความต้องการออกซิเจน) หรือปริมาณไขมันเกินมาตรฐาน อาจนำมาซึ่งการเสียค่าปรับครั้งใหญ่ หรือกระทบต่อใบอนุญาตประกอบกิจการ 📉

แต่นอกจากเรื่องข้อกฎหมายแล้ว "กลิ่นไม่พึงประสงค์จากระบบบำบัดน้ำเสีย (STP)" ยังเป็นภัยเงียบที่ทำลายความประทับใจของแขกผู้เข้าพักได้ในทันที และส่งผลลบต่อภาพลักษณ์โรงแรมหรูอย่างรุนแรง

การบำบัดน้ำเสียด้วยสารเคมีอาจส่งผลเสียต่อแบคทีเรียธรรมชาติในระบบบำบัด ทำให้ระบบล่มและไม่ได้ผลลัพธ์ที่ยั่งยืน
โรงแรมชั้นนำในปัจจุบันจึงหันมาใช้แนวคิดเทคโนโลยีชีวภาพสีเขียว (Green Biotechnology) ด้วยการใช้จุลินทรีย์ธรรมชาติประสิทธิภาพสูงช่วยควบคุมระบบบำบัดตลอด 24 ชั่วโมง เพื่อย่อยสลายสารอินทรีย์และปรับค่าน้ำทิ้งให้ผ่านเกณฑ์มาตรฐานอย่างเป็นธรรมชาติและยั่งยืน

ยกระดับภาพลักษณ์โรงแรมหรูสู่มาตรฐานสิ่งแวดล้อมระดับสากล (BCG Model)

📂 อ่านแนวทางการบำบัดน้ำทิ้งโรงแรมและสไลด์พรีเซนต์ระดับหรู:
👉 https://biorevive-lab.vercel.app/pitch_deck_hotel.html

💬 ปรึกษาวิศวกรสิ่งแวดล้อม LINE OA: @biorevivelab
#มาตรฐานน้ำทิ้ง #โรงแรมหรู #ระบบบำบัดน้ำเสีย #BCGModel #ความยั่งยืน #BioReviveLab"""

    # Target timestamps for today
    now = datetime.now()
    
    # 09:59
    t1 = datetime(now.year, now.month, now.day, 9, 59, 0)
    # 14:59
    t2 = datetime(now.year, now.month, now.day, 14, 59, 0)
    # 19:59
    t3 = datetime(now.year, now.month, now.day, 19, 59, 0)

    # Schedule posts
    schedule_post("assets/chk_sink.png", ep1_caption, t1.timestamp())
    schedule_post("assets/chk_grease.png", ep2_caption, t2.timestamp())
    schedule_post("assets/chk_pit.png", ep3_caption, t3.timestamp())
