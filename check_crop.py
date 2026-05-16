from PIL import Image
import os

def check_raw_crop():
    img_path = 'assets/fb_post_teabag.png'
    try:
        img = Image.open(img_path)
        # Much larger crop to be safe
        w, h = img.size
        # Center is around (w/2, h/2)
        # Bag is slightly lower
        left = int(w * 0.1)
        top = int(h * 0.2)
        right = int(w * 0.9)
        bottom = int(h * 0.98)
        
        raw_crop = img.crop((left, top, right, bottom))
        raw_crop.save(r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\raw_crop_test.png')
        print("Raw crop saved. Check if teabags are visible here.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_raw_crop()
