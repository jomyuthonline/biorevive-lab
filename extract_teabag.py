from rembg import remove
from PIL import Image
import os

def extract_and_replace():
    input_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\temp_crop.png'
    output_path = 'assets/ad_teabag_final.png'
    
    try:
        print("Loading image for background removal...")
        img = Image.open(input_path)
        
        print("Running rembg...")
        # Remove background
        img_nobg = remove(img).convert("RGBA")
        
        print("Cropping to bounding box...")
        # Get bounding box of non-transparent pixels
        bbox = img_nobg.getbbox()
        if bbox:
            img_nobg = img_nobg.crop(bbox)
            
        # Save over ad_teabag_final.png
        img_nobg.save(output_path)
        print(f"Success! Replaced {output_path} with the new extracted product.")
        
        # Also copy to artifact folder for preview
        preview_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\ad_teabag_final_preview.png'
        img_nobg.save(preview_path)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_and_replace()
