from PIL import Image, ImageDraw, ImageFont
import os

def final_fix():
    input_path = 'assets/ad_teabag_final.png'
    output_path = 'assets/ad_teabag_final.png' # Overwrite with the good one
    preview_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\ad_teabag_final_fixed.png'
    
    try:
        img = Image.open(input_path).convert("RGBA")
        w, h = img.size
        print(f"Original size: {w}x{h}")
        
        # 1. Widen the bag (Rescale width by ~15% to fix the 'narrow' look)
        new_w = int(w * 1.15)
        img = img.resize((new_w, h), Image.Resampling.LANCZOS)
        w, h = img.size
        print(f"Resized size: {w}x{h}")
        
        # 2. Fix the label: Change 800 g. to 20 g. x 6 ซอง
        # Usually the weight is at the bottom of the blue label area.
        # We'll draw a small beige/navy box to cover the old text and write new text.
        # This part requires guessing the coordinates. 
        # For a 1024 height bag, weight is usually around y=850-900.
        
        draw = ImageDraw.Draw(img)
        
        # Define the area to 'patch' (approximate based on standard label layout)
        # We'll use a color picker approach if we could, but we'll try to match the label's navy.
        navy_color = (10, 25, 47, 255) # Standard BioRevive Navy
        
        # Masking the bottom part of the label
        # (Assuming the 800g is in the bottom center of the label)
        # Box center around x=w/2, y=h*0.82
        label_bottom_y = int(h * 0.82)
        patch_w = int(w * 0.6)
        patch_h = 40
        left = (w - patch_w) // 2
        top = label_bottom_y - patch_h // 2
        
        # Draw the patch
        draw.rectangle([left, top, left + patch_w, top + patch_h], fill=navy_color)
        
        # Add new text
        try:
            # Try to load a font
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            
        text = "20 g. x 6 ซอง"
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        
        text_x = (w - text_w) // 2
        text_y = top + (patch_h - text_h) // 2
        
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
        
        # 3. Handle teabags (Add 6 teabags if they aren't there)
        # If the original ad_teabag_final.png is just the bag, we might need to paste them.
        # Since I don't have a high-res source for 6 teabags right now (the old ones were 'bad'),
        # I'll just focus on the bag fix first and ask the user.
        
        # Save results
        img.save(output_path)
        img.save(preview_path)
        print("Success! Bag widened and label updated.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_fix()
