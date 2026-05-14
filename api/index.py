import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    FlexSendMessage
)

app = Flask(__name__)

# --- ข้อมูลการเชื่อมต่อ ---
CHANNEL_ACCESS_TOKEN = 'cpph9jimA8eWFSV+T5Drmq75NkGWMILBtIjtdC2eUwuJDWUgnqjUoPrV3NjYoGWLBxk4UTaxDOtz6hUGsfSbDxzsCxAg0JLLmXma155c52eyOvJTJLU/rm7oGSGs8ZShjLc2JUGjo4XSxgTwwNNNggdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '055a435a7d7050470e27bf5d47b9ae76'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

BASE_URL = "https://biorevive-lab.vercel.app"

# --- ฐานข้อมูลคำตอบแบบละเอียด ---
DETAILS = {
    "ความเชี่ยวชาญ 20 ปี": "🏆 ประวัติและความเชี่ยวชาญ:\nBioRevive Lab ต่อยอดเทคโนโลยีจุลินทรีย์ธรรมชาติจากประสบการณ์กว่า 20 ปี ในการเป็นที่ปรึกษาด้านระบบนิเวศให้กับฟาร์มกุ้งและภาคเกษตรกรรมชั้นนำของไทย\n\nเรานำนวัตกรรม 'เชื้อสด' มาปรับใช้เพื่อแก้ไขปัญหากลิ่นและไขมันในภาคบริการ (โรงแรม/ร้านอาหาร) อย่างยั่งยืนและปลอดภัย 100% ครับ",
    
    "3 พลังเอนไซม์": "🧬 นวัตกรรม 3 Enzymes:\nจุลินทรีย์เชื้อสดของเราผลิตเอนไซม์เข้มข้น 3 ชนิดที่ทำงานทันที:\n1. Lipase: ย่อยสลายคราบไขมัน (Fat/Oil)\n2. Protease: ย่อยสลายกากโปรตีนและเนื้อสัตว์\n3. Amylase: ย่อยสลายแป้งและเศษอาหาร\n\n*ทำให้กลิ่นหายขาดใน 24 ชม. และไขมันไม่อุดตันถาวรครับ*",
    
    "วิธีการใช้งาน": "✅ วิธีใช้ BioRevive Lab:\n\n💧 1. สูตรน้ำ (Liquid): เหมาะสำหรับล้างระบบและดับกลิ่นเร่งด่วน เทลงท่อ/ซิงค์ 50-500 มล. หลังปิดร้าน\n\n💎 2. สูตรพรีเมี่ยม (Premium/Tea Bag): สำหรับถังดักไขมัน วางซองชาที่จุดน้ำไหลผ่าน หรือเทผงพรีเมี่ยมเพื่อสลายไขมันสะสมหนา\n\n💡 แนะนำ: ใช้ช่วงน้ำนิ่ง (หลังปิดร้าน) เพื่อให้จุลินทรีย์ทำงานได้เต็มที่ครับ",
    
    "ระยะเวลาเห็นผล": "⏳ ระยะเวลา:\n- กลิ่นเหม็น: ลดลงทันทีและหายขาดใน 24 ชั่วโมง\n- ไขมันอุดตัน: เริ่มอ่อนตัวและเล็กลงใน 3-7 วัน\n\nหากใช้ต่อเนื่อง จะช่วยประหยัดค่าบริการรถดูดไขมันได้มากกว่า 50% ต่อปีครับ",
    
    "ปลอดภัย & BCG": "🌿 มาตรฐานความปลอดภัย:\n- Organic 100% ปลอดภัยต่อผู้ใช้งาน\n- ไม่กัดกร่อนท่อ (Non-Corrosive)\n- สอดคล้องกับมาตรฐาน BCG Model และ Green Restaurant\n- มีใบรับรองค่า BOD/SS ตามกฎหมายควบคุมมลพิษครับ",
    
    "นัดหมายประเมินฟรี": "📸 บริการประเมินหน้างานฟรี!:\nเพื่อการคำนวณปริมาณที่แม่นยำ ท่านสามารถ:\n1. ส่งรูปถังดักไขมัน/หน้างาน\n2. ระบุเบอร์โทรติดต่อกลับ\n\nผู้เชี่ยวชาญของเราจะรีบวิเคราะห์และเสนอโซลูชั่นที่คุ้มค่าที่สุดให้ภายในวันนี้ครับ"
}

def create_bubble(title, text, btn_text, img_url=None, url=None):
    bubble = {
        "type": "bubble", "size": "micro",
        "header": {
            "type": "box", "layout": "vertical", "backgroundColor": "#162C4E",
            "contents": [{"type": "text", "text": title, "weight": "bold", "size": "sm", "color": "#C5A059"}]
        }
    }
    
    if img_url:
        bubble["hero"] = {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        }
        
    bubble["body"] = {
        "type": "box", "layout": "vertical", "contents": [{"type": "text", "text": text, "wrap": True, "size": "xs", "color": "#4A5568"}]
    }
    
    bubble["footer"] = {
        "type": "box", "layout": "vertical",
        "contents": [{
            "type": "button", "style": "primary", "color": "#C5A059", "height": "sm",
            "action": {
                "type": "uri" if url else "message",
                "label": btn_text,
                "uri": url if url else None,
                "text": None if url else "สอบถามเรื่อง: " + title
            }
        }]
    }
    return bubble

def get_faq_carousel():
    return {
        "type": "carousel",
        "contents": [
            create_bubble("3 พลังเอนไซม์", "สลายไขมันสะสมด้วยจุลินทรีย์เชื้อสด", "ดูการทำงาน", f"{BASE_URL}/assets/story_solution.png"),
            create_bubble("วิธีการใช้งาน", "เทคนิคใช้ให้เห็นผลไวที่สุด", "วิธีใช้ละเอียด", f"{BASE_URL}/assets/ad_liquid.png"),
            create_bubble("ความเชี่ยวชาญ 20 ปี", "ผู้นำเทคโนโลยีชีวภาพเพื่อสิ่งแวดล้อม", "ดูประวัติเรา", f"{BASE_URL}/assets/restaurant.png"),
            create_bubble("ระยะเวลาเห็นผล", "กลิ่นหายใน 24 ชม. ไขมันลดใน 7 วัน", "เช็คประสิทธิภาพ", f"{BASE_URL}/assets/warn_canal.png"),
            create_bubble("ปลอดภัย & BCG", "รักษ์โลก 100% ไม่กัดท่อ ไม่กัดมือ", "ดูใบรับรอง", f"{BASE_URL}/assets/hotel.png"),
            create_bubble("ประเมินความเสี่ยง", "ตรวจสอบ 5 จุดเสี่ยงออนไลน์ (ฟรี)", "เริ่มตรวจเช็ค", f"{BASE_URL}/assets/hidden_crisis_th.png", f"{BASE_URL}/checklist.html"),
            create_bubble("นัดหมายประเมินฟรี", "ส่งรูปหน้างานให้ผู้เชี่ยวชาญช่วยดู", "คุยกับผู้เชี่ยวชาญ", f"{BASE_URL}/assets/grease_trap.png")
        ]
    }

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    if "สอบถามเรื่อง: " in user_text:
        topic = user_text.replace("สอบถามเรื่อง: ", "")
        if topic in DETAILS:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=DETAILS[topic]))
            return

    if "สนใจสั่งซื้อ" in user_text:
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="ขอบพระคุณที่สนใจสั่งซื้อ BioRevive Lab ครับ! 🙏\n\nเจ้าหน้าที่ได้รับข้อมูลรายการสั่งซื้อของท่านแล้วครับ กำลังรีบตรวจสอบสต็อกและเตรียมสรุปยอดให้ท่านในทันที รบกวนรอสักครู่นะครับ 🐆✨"),
            TextSendMessage(text="ระหว่างรอ ท่านสามารถส่งรูป 'หน้างาน' หรือ 'ถังดักไขมัน' มาให้เราช่วยประเมินการใช้งานที่เหมาะสมที่สุดได้ฟรีนะครับ")
        ])
        return

    responses = {
        "กลิ่น": DETAILS["ระยะเวลาเห็นผล"],
        "ราคา": "ราคาเริ่มต้นเพียง 299.- ถึง 611.- ครับ หากรับปริมาณมาก (Set L) หรือใช้ในโปรเจกต์โรงแรม มีราคาพิเศษสำหรับพาร์ทเนอร์ครับ ทักแชทหาเจ้าหน้าที่ได้เลย",
        "เอนไซม์": DETAILS["3 พลังเอนไซม์"],
        "เชื้อสด": "BioRevive เป็นจุลินทรีย์เชื้อสดที่ทำงานทันที สลายไขมันและกลิ่นใน 24 ชม. ครับ",
        "ประวัติ": DETAILS["ความเชี่ยวชาญ 20 ปี"],
        "bcg": DETAILS["ปลอดภัย & BCG"],
        "ปลอดภัย": DETAILS["ปลอดภัย & BCG"]
    }

    for key in responses:
        if key in user_text.lower():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=responses[key]))
            return

    greetings = ["สวัสดี", "เมนู", "hi", "hello", "เริ่ม", "สอบถาม", "เริ่มต้น", "เมนูหลัก"]
    if any(greet in user_text.lower() for greet in greetings):
        flex_msg = FlexSendMessage(alt_text="เมนูช่วยเหลือ BioRevive Lab", contents=get_faq_carousel())
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="สวัสดีครับ BioRevive Lab ยินดีให้บริการครับ! 🌱\nเราคือผู้เชี่ยวชาญด้านจุลินทรีย์เชื้อสดกว่า 20 ปี ท่านสามารถเลือกหัวข้อที่สนใจด้านล่างได้เลยครับ"),
            flex_msg
        ])

if __name__ == "__main__":
    app.run(port=5000)
