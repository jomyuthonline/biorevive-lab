import os
from gtts import gTTS

def generate_voiceovers():
    # Target directory
    assets_dir = os.path.join(os.getcwd(), 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Liquid Series Voiceover Text
    liquid_text = (
        "ไบโอ รีไวฟ์ แล็บ รุ่น ลิควิด ซีรีส์! สูตรน้ำเข้มข้นแอคทีฟพิเศษ "
        "ย่อยสลายไขมันสะสมในท่อระบายน้ำและถังดักได้ทันที รวดเร็ว ปลอดภัย "
        "ไร้กลิ่นเหม็นเน่ารบกวน คืนสุขอนามัยที่ดีด้วยพลังธรรมชาติ 100% "
        "ติดต่อปรึกษาปัญหาน้ำทิ้งได้ที่ ไลน์ แอด ไบโอ รีไวฟ์ แล็บ ครับ"
    )
    
    # 2. Premium Series Voiceover Text
    premium_text = (
        "ไบโอ รีไวฟ์ แล็บ รุ่น พรีเมียม ซีรีส์! หัวเชื้อจุลินทรีย์ชนิดแห้ง "
        "เข้มข้นแอคทีฟสูงสุด สะดวกด้วยรุ่นซองชา 20 กรัม ทรงพลังด้วยรุ่นถุง 1 กิโลกรัม "
        "และคุ้มค่าสูงสุดด้วยรุ่นถังใหญ่ 6 กิโลกรัม เหมาะสำหรับโรงแรมและบ่อเอสทีพีขนาดใหญ่ "
        "ปลอดภัยต่อท่อ 100% สั่งซื้อเลยครับ"
    )
    
    # Generate Liquid Voiceover
    print("Generating liquid series voiceover...")
    tts_liquid = gTTS(text=liquid_text, lang='th')
    liquid_path = os.path.join(assets_dir, 'voiceover_liquid.mp3')
    tts_liquid.save(liquid_path)
    print(f"Liquid voiceover saved to: {liquid_path}")
    
    # Generate Premium Voiceover
    print("Generating premium series voiceover...")
    tts_premium = gTTS(text=premium_text, lang='th')
    premium_path = os.path.join(assets_dir, 'voiceover_premium.mp3')
    tts_premium.save(premium_path)
    print(f"Premium voiceover saved to: {premium_path}")

if __name__ == '__main__':
    generate_voiceovers()
