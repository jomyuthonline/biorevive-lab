from PIL import Image
import os

def crop_product():
    img_path = 'assets/fb_post_teabag.png'
    try:
        img = Image.open(img_path)
        w, h = img.size
        print(f"Image size: {w}x{h}")
        
        # Estimate crop box based on typical 1080x1080 layout
        # Bag is usually in the center bottom half
        left = int(w * 0.15)
        top = int(h * 0.25)
        right = int(w * 0.85)
        bottom = int(h * 0.95)
        
        crop_box = (left, top, right, bottom)
        cropped_img = img.crop(crop_box)
        
        # Save to artifact folder for preview
        artifact_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\temp_crop.png'
        cropped_img.save(artifact_path)
        print(f"Cropped image saved to {artifact_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    crop_product()
