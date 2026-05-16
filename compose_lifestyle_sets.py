from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os

# Paths
ASSETS_DIR = r"C:\BioRevive_Master\assets"
OUTPUT_DIR = ASSETS_DIR

# Products (Verified Nobg versions)
PROD_1L = os.path.join(ASSETS_DIR, "ad_liquid_1l_nobg.png")
PROD_5L = os.path.join(ASSETS_DIR, "ad_liquid_5l_nobg.png")
PROD_1KG = os.path.join(ASSETS_DIR, "ad_pouch_white_1kg_nobg.png")
PROD_6KG = os.path.join(ASSETS_DIR, "ad_bucket_6kg_nobg.png")
PROD_TEABAG = os.path.join(ASSETS_DIR, "ad_teabag_with_6teabags_nobg.png")

# Backgrounds
BG_S = os.path.join(ASSETS_DIR, "cafe.png")
BG_M = os.path.join(ASSETS_DIR, "restaurant.png")
BG_L = os.path.join(ASSETS_DIR, "hotel.png")

def create_lifestyle_set(name, bg_path, products, output_filename):
    print(f"Creating Lifestyle {name}...")
    bg = Image.new("RGBA", (1024, 1024), (255,255,255,255))
    orig_bg = Image.open(bg_path).convert("RGBA")
    
    # Blur background slightly to make products pop, but less than before
    orig_bg = orig_bg.filter(ImageFilter.GaussianBlur(radius=2))
    
    # Darken background slightly (0.85 instead of 0.7 for more vibrancy)
    enhancer = ImageEnhance.Brightness(orig_bg)
    orig_bg = enhancer.enhance(0.85)
    
    # Paste bg onto canvas
    bg.paste(orig_bg.resize((1024, 1024), Image.Resampling.LANCZOS), (0,0))
    
    # Sort products by Y (back to front to draw correctly)
    products.sort(key=lambda x: x[1][1])
    
    for p_path, pos, scale in products:
        p_img = Image.open(p_path).convert("RGBA")
        new_w = int(p_img.width * scale)
        new_h = int(p_img.height * scale)
        p_img = p_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        x, y = pos
        
        # 1. Soft Drop Shadow (Removes the "bad die-cut" hard edge)
        blur_radius = 25
        shadow_img = Image.new("RGBA", (new_w + blur_radius*2, new_h + blur_radius*2), (0, 0, 0, 0))
        shadow_mask = p_img.split()[3]
        shadow_solid = Image.new("RGBA", p_img.size, (0, 0, 0, 110))
        shadow_img.paste(shadow_solid, (blur_radius, blur_radius), mask=shadow_mask)
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Paste soft drop shadow slightly offset
        bg.alpha_composite(shadow_img, (x - blur_radius + 5, y - blur_radius + 15))

        # 2. Contact Shadow (Dark ellipse under the object to ground it)
        shadow_w = int(new_w * 0.7)
        shadow_h = int(new_h * 0.1)
        contact_shadow = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(contact_shadow)
        shadow_x0 = int((new_w - shadow_w) / 2)
        shadow_y0 = new_h - shadow_h + 10
        draw.ellipse([shadow_x0, shadow_y0, shadow_x0 + shadow_w, shadow_y0 + shadow_h], fill=(0, 0, 0, 160))
        contact_shadow = contact_shadow.filter(ImageFilter.GaussianBlur(10))
        
        # Place the contact shadow at the base
        bg.alpha_composite(contact_shadow, (x, y))
        
        # Paste Product
        bg.alpha_composite(p_img, pos)

    bg.save(os.path.join(OUTPUT_DIR, output_filename))
    print(f"Saved {output_filename}")

# Define Lifestyle Sets with adjusted scales and grounded positions
# Y positions are adjusted so the bases align better, giving a realistic table-top perspective.

# Set S: Home/Cafe
create_lifestyle_set("Set S", BG_S, [
    (PROD_1L, (220, 350), 0.75),
    (PROD_TEABAG, (480, 500), 0.7)
], "promo_set_s_lifestyle.png")

# Set M: Restaurant
create_lifestyle_set("Set M", BG_M, [
    (PROD_5L, (150, 320), 0.65),
    (PROD_1KG, (450, 420), 0.65),
    (PROD_TEABAG, (620, 560), 0.55)
], "promo_set_m_lifestyle.png")

# Set L: Hotel
create_lifestyle_set("Set L", BG_L, [
    (PROD_5L, (80, 350), 0.55),
    (PROD_5L, (230, 350), 0.55),
    (PROD_6KG, (450, 250), 0.75),
    (PROD_TEABAG, (180, 620), 0.5),
    (PROD_TEABAG, (400, 620), 0.5),
    (PROD_TEABAG, (620, 620), 0.5)
], "promo_set_l_lifestyle.png")
