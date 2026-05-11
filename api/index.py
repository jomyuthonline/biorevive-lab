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

# --- ฐานข้อมูลคำตอบแบบละเอียด ---
DETAILS = {
    "วิธีการใช้งาน": "✅ วิธีใช้ BioRevive Lab - ไบโอรีไวฟ์ แลปส์:\n\n💎 1. จุลินทรีย์เชื้อสด สูตรพรีเมี่ยม (Active Microbes - Premium)\n(แบบเนื้อสดเข้มข้น 1 kg./6 kg. และ แบบซองชา 20g. x 6)\n📍 สำหรับล้างระบบช่วงเริ่มต้นหรือแก้ปัญหาหนัก: เท 100 กรัม (3-4 ช้อนโต๊ะ) ลงชักโครกหรือถังดักไขมัน หรือวางซองชาที่จุดน้ำไหลผ่านครับ\n\n💧 2. จุลินทรีย์เชื้อสด สูตรน้ำ (Active Microbes - Liquid)\n(ขนาด 1 L./5 L.)\n📍 สำหรับดูแลรักษาสมดุลประจำวัน: เทลงท่อ/อ่างซิงค์ 50-500 มล. หรือผสมน้ำถูพื้นครัวได้ครับ\n\n💡 คำแนะนำ: ในช่วง 1-2 สัปดาห์แรก ควรเติมต่อเนื่อง 5-6 วันเพื่อให้จุลินทรีย์เคลียร์ระบบได้เต็มประสิทธิภาพครับ",
    "ระยะเวลาเห็นผล": "⏳ ระยะเวลา:\n- กลิ่นเหม็น: หายขาดใน 24 ชั่วโมง\n- ไขมันสะสม: จะเริ่มอ่อนตัวและย่อยสลายใน 3-7 วันครับ\n*ด้วยนวัตกรรมเชื้อสด BioRevive Lab เห็นผลชัดเจนและปลอดภัย 100% ครับ*",
    "ปริมาณที่แนะนำ": "📏 ปริมาณการใช้:\nขึ้นอยู่กับขนาดถังดักไขมันและภาระงานของร้านครับ รบกวนแจ้งขนาดถังหรือส่งรูปหน้างานให้นักวิชาการ BioRevive Lab ช่วยคำนวณปริมาณที่เหมาะสมที่สุดให้ได้เลยครับ",
    "ปลอดภัย 100%": "🛡️ มาตรฐานความปลอดภัย:\nจุลินทรีย์ BioRevive Lab เป็น Organic 100% ไม่กัดกร่อนท่อ ไม่ทำลายมือผู้ใช้ และปลอดภัยต่อคน/สัตว์เลี้ยงครับ (มีผลตรวจรับรองมาตรฐานกฎหมาย BOD/SS)",
    "นวัตกรรมเชื้อสด": "🧬 ทำไมต้องเชื้อสด?:\nต่างจากจุลินทรีย์แบบผงแห้งทั่วไปที่ต้องรอการ 'ฟักตัว' นานหลายชั่วโมง เชื้อสด BioRevive Lab ทำงานได้ทันทีที่สัมผัสสิ่งปฏิกูล ประสิทธิภาพจึงสูงและสยบกลิ่นได้ไวที่สุดครับ",
    "นัดหมายปรึกษาฟรี": "📅 นัดหมายพูดคุย:\nท่านสามารถพิมพ์ระบุ 'วันและเวลา' ที่สะดวกไว้ได้เลยครับ เพื่อให้นักวิชาการจาก BioRevive Lab ติดต่อกลับเพื่อประเมินหน้างานฟรีครับ"
}

def get_faq_carousel():
    return {
        "type": "carousel",
        "contents": [
            create_bubble("วิธีการใช้งาน", "แบบเทและแบบวาง ง่ายและสะดวก", "สอบถามวิธีใช้"),
            create_bubble("ระยะเวลาเห็นผล", "สยบกลิ่นใน 24 ชม. เห็นผลชัดเจน", "ปรึกษาความเร็ว"),
            create_bubble("ปริมาณที่แนะนำ", "ช่วยคำนวณตามขนาดหน้างาน", "ส่งรูปประเมิน"),
            create_bubble("ปลอดภัย 100%", "Organic 100% ไม่กัดมือ ไม่กัดท่อ", "ดูมาตรฐาน"),
            create_bubble("นวัตกรรมเชื้อสด", "ทำงานทันที ไม่ต้องรอฟักตัวเหมือนแบบผง", "ทำไมถึงดีกว่า"),
            create_bubble("ประเมินความเสี่ยง", "ตรวจสอบ 5 จุดเสี่ยงระบบน้ำทิ้งออนไลน์", "เริ่มประเมิน", "https://biorevive-lab.vercel.app/checklist.html"),
            create_bubble("นัดหมายปรึกษาฟรี", "ลงวันนัดให้เจ้าหน้าที่ติดต่อกลับ", "ลงวันนัดหมาย")
        ]
    }

def create_bubble(title, text, btn_text, url=None):
    return {
        "type": "bubble", "size": "micro",
        "header": {
            "type": "box", "layout": "vertical", "backgroundColor": "#001f3f",
            "contents": [{"type": "text", "text": title, "weight": "bold", "size": "sm", "color": "#d4af37"}]
        },
        "body": {
            "type": "box", "layout": "vertical", "contents": [{"type": "text", "text": text, "wrap": True, "size": "xs", "color": "#666666"}]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [{
                "type": "button", "style": "primary", "color": "#d4af37", "height": "sm",
                "action": {
                    "type": "uri" if url else "message",
                    "label": btn_text,
                    "uri": url if url else None,
                    "text": None if url else "สอบถามเรื่อง: " + title
                }
            }]
        }
    }

# Route สำหรับ LINE Bot callback เท่านั้น (หน้าเว็บหลักจะใช้ index.html ปกติ)
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
    user_text = event.message.text
    
    # 1. เช็คว่าเป็นการกดปุ่มจากเมนูหรือไม่
    if "สอบถามเรื่อง: " in user_text:
        topic = user_text.replace("สอบถามเรื่อง: ", "")
        if topic in DETAILS:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=DETAILS[topic]))
            return

    # 2. เช็คว่าเป็นข้อความสั่งซื้อจากหน้าเว็บหรือไม่
    if "สนใจสั่งซื้อ" in user_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ขอบพระคุณที่สนใจสั่งซื้อ BioRevive Lab ครับ! 🙏\n\nเจ้าหน้าที่ได้รับข้อมูลรายการของท่านแล้ว กำลังรีบตรวจสอบสต็อกและสรุปยอดโอนให้ท่านภายใน 1-3 นาทีนี้ครับ รบกวนรอสักครู่นะครับ 🐆✨"))
        return

    # 3. เช็ค Keywords ทั่วไป
    responses = {
        "กลิ่น": DETAILS["ระยะเวลาเห็นผล"],
        "ราคา": "จุลินทรีย์เริ่มต้นเพียง 299.- สนใจรับใบเสนอราคาพิเศษทักแชทหาเจ้าหน้าที่ได้เลยครับ",
        "bcg": "BioRevive Lab ตอบโจทย์นโยบาย BCG และ ESG รักษ์โลก 100% ครับ",
        "กฎหมาย": DETAILS["ปลอดภัย 100%"]
    }

    for key in responses:
        if key in user_text.lower():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=responses[key]))
            return

    # 3. ถ้าไม่เข้าเงื่อนไขเลย ให้ตรวจสอบว่าเป็นคำทักทายหรือไม่
    greetings = ["สวัสดี", "เมนู", "hi", "hello", "เริ่ม", "สอบถาม", "เริ่มต้น"]
    if any(greet in user_text.lower() for greet in greetings):
        flex_msg = FlexSendMessage(alt_text="เมนูช่วยเหลือ BioRevive Lab", contents=get_faq_carousel())
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="สวัสดีครับ BioRevive Lab ยินดีให้บริการครับ! 🌱\nหากท่านมีข้อสงสัย สามารถเลือกหัวข้อที่ต้องการทราบข้อมูลได้เลยครับ"),
            flex_msg
        ])
    # ถ้าไม่ใช่คำทักทายและไม่ติด Keyword อื่นๆ จะไม่ตอบอะไรเลย (เพื่อให้เจ้าหน้าที่ตอบเอง)

if __name__ == "__main__":
    app.run(port=5000)
