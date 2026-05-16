from rembg import remove
from PIL import Image
import os

def fix_extraction():
    input_path = 'assets/fb_post_teabag.png'
    output_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\full_nobg_test.png'
    
    try:
        print(f"Loading {input_path}...")
        img = Image.open(input_path)
        
        print("Running rembg on full image...")
        # Remove background from full image to preserve all elements
        img_nobg = remove(img).convert("RGBA")
        
        # Save for preview
        img_nobg.save(output_path)
        print(f"Full background removal saved to {output_path}")
        
        # Now find the bounding box of EVERYTHING that remains
        bbox = img_nobg.getbbox()
        if bbox:
            print(f"Bounding box: {bbox}")
            final_product = img_nobg.crop(bbox)
            final_product.save('assets/ad_teabag_final.png')
            final_product.save(r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\ad_teabag_final_v2.png')
            print("Successfully updated assets/ad_teabag_final.png with full crop.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_extraction()
