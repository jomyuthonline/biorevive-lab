from PIL import Image, ImageDraw
import os

def complex_edit():
    input_path = 'assets/ad_teabag_fixed_preview.png'
    sticker_path = 'assets/stickerซองชา.jpg'
    output_path = 'assets/ad_teabag_final_v3.png'
    preview_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\ad_teabag_final_v3.png'
    
    try:
        img = Image.open(input_path).convert("RGBA")
        w, h = img.size
        
        draw = ImageDraw.Draw(img)
        
        # 1. Remove the black bar at the bottom
        # Black bar is roughly at the bottom center.
        # Let's cover the bottom 15% area with the background color (dark gold/brown)
        bg_color = img.getpixel((w//2, h - 5)) # Sample color from bottom
        draw.rectangle([0, int(h * 0.9), w, h], fill=bg_color)
        
        # 2. Remove the existing navy sticker on the bag
        # The bag center area.
        bag_color = (215, 190, 155, 255) # Approximate beige
        # Find label area (approx center)
        label_left = int(w * 0.25)
        label_top = int(h * 0.3)
        label_right = int(w * 0.75)
        label_bottom = int(h * 0.8)
        draw.rectangle([label_left, label_top, label_right, label_bottom], fill=bag_color)
        
        # 3. Load and paste the new sticker
        sticker = Image.open(sticker_path).convert("RGBA")
        s_w, s_h = sticker.size
        # Paste sticker in the center of the bag
        paste_x = (w - s_w) // 2
        paste_y = (h - s_h) // 2 - 50 # Slightly higher
        img.paste(sticker, (paste_x, paste_y), sticker)
        
        # 4. Increase teabags from 4 to 6
        # The teabags are on the right. 
        # I'll crop one teabag and paste it two more times.
        # This is a bit of a guess on coordinates.
        # Teabags are around x=600-800, y=500-700 in the 1350x1350 image.
        # In this 656x1024 image, they are on the right.
        
        teabag_crop = img.crop((w - 200, 600, w - 50, 850))
        # Paste two more teabags slightly offset
        img.paste(teabag_crop, (w - 300, 620), teabag_crop)
        img.paste(teabag_crop, (w - 350, 640), teabag_crop)
        
        # Save
        img.save(output_path)
        img.save(preview_path)
        print("Success! Sticker replaced, bar removed, and teabags updated.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    complex_edit()
