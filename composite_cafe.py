from rembg import remove
from PIL import Image, ImageFilter
import os

def create_natural_post():
    try:
        # 1. Load correct product image and remove background
        input_product_path = 'assets/ad_teabag_6pcs.png'
        print(f"Processing background removal for: {input_product_path}")
        product_raw = Image.open(input_product_path)
        product_nobg = remove(product_raw).convert("RGBA")
        
        # Save transparent version for future use
        product_nobg.save('assets/product_teabag_6pcs_nobg.png')
        print("Saved transparent product to assets/product_teabag_6pcs_nobg.png")

        # 2. Load background image
        bg = Image.open('assets/ad_cafe.png').convert("RGBA")
        bg_w, bg_h = bg.size
        
        # 3. Resize product to look natural on the counter
        target_h = int(bg_h * 0.28)
        aspect_ratio = product_nobg.width / product_nobg.height
        target_w = int(target_h * aspect_ratio)
        product = product_nobg.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # 4. Position on the marble counter
        pos_x = int(bg_w * 0.15)
        pos_y = int(bg_h * 0.72)
        
        # 5. Create a subtle drop shadow
        shadow = Image.new('RGBA', product.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 180), mask=product.split()[3]) 
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        
        # Composite shadow and product
        shadow_offset_x = 5
        shadow_offset_y = 20
        bg.paste(shadow, (pos_x + shadow_offset_x, pos_y + shadow_offset_y), shadow)
        bg.paste(product, (pos_x, pos_y), product)
        
        # 6. Adjust Color Grading slightly (Warm up the product to match cafe)
        # We can blend a tiny bit of orange into the product to match cafe lighting
        # Skipping complex color grading to ensure clarity, shadow is usually enough for a soft-sell
        
        # Save final
        final_img = bg.convert("RGB")
        final_img.save('assets/fb_post_cafe_softsell.png')
        print("Success: Generated assets/fb_post_cafe_softsell.png")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_natural_post()
