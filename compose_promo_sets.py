from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os

# Paths
ASSETS_DIR = r"C:\BioRevive_Master\assets"
CATALOG_DIR = os.path.join(ASSETS_DIR, "catalog")
OUTPUT_DIR = ASSETS_DIR

# Products from the catalog folder (transparent cutout versions)
PROD_1L = os.path.join(ASSETS_DIR, "ad_liquid_1l_nobg.png")
PROD_5L = os.path.join(ASSETS_DIR, "ad_liquid_5l_nobg.png")
PROD_1KG = os.path.join(ASSETS_DIR, "ad_pouch_white_1kg_nobg.png")
PROD_6KG = os.path.join(ASSETS_DIR, "ad_bucket_6kg_nobg.png")
PROD_TEABAG = os.path.join(ASSETS_DIR, "ad_teabag_with_6teabags_nobg.png")

def create_set_v3(name, products, output_filename):
    print(f"Creating Premium Catalog {name}...")
    w, h = 1024, 1024
    
    # 1. Premium Deep Navy & Gold Radial Gradient Background
    final = Image.new("RGBA", (w, h), (10, 20, 38, 255))
    draw = ImageDraw.Draw(final)
    
    # Draw linear gradient first
    for y in range(h):
        r = int(10 + (16 - 10) * (y / h))
        g = int(20 + (32 - 20) * (y / h))
        b = int(38 + (58 - 38) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
    
    # Add beautiful golden radial halo glow in center to highlight the product pack
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    # Center circle for gold aura
    halo_draw.ellipse([w*0.2, h*0.2, w*0.8, h*0.8], fill=(197, 160, 89, 25))
    final.alpha_composite(halo.filter(ImageFilter.GaussianBlur(80)))
    
    # Add subtle luxury geometric accent lines in gold
    gold_color = (197, 160, 89, 40)
    draw.line([(0, h*0.15), (w, h*0.05)], fill=gold_color, width=1)
    draw.line([(0, h*0.85), (w, h*0.95)], fill=gold_color, width=1)
    draw.arc([w*0.05, h*0.05, w*0.95, h*0.95], start=0, end=360, fill=(197, 160, 89, 15), width=1)

    # 2. Add realistic ground shadow / floor glow
    floor_glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(floor_glow)
    fg_draw.ellipse([w*0.1, h*0.7, w*0.9, h*0.95], fill=(255, 255, 255, 8))
    final.alpha_composite(floor_glow.filter(ImageFilter.GaussianBlur(40)))

    # Sort products by Y coordinate so they render back-to-front
    products.sort(key=lambda x: x[1][1])
    
    for p_path, pos, scale in products:
        p_img = Image.open(p_path).convert("RGBA")
        new_w = int(p_img.width * scale)
        new_h = int(p_img.height * scale)
        p_img = p_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        x, y = pos
        
        # 1. Realistic Soft Drop Shadow for luxury pop
        shadow_blur = 30
        shadow_img = Image.new("RGBA", (new_w + shadow_blur*2, new_h + shadow_blur*2), (0, 0, 0, 0))
        shadow_mask = p_img.split()[3]
        shadow_solid = Image.new("RGBA", p_img.size, (0, 0, 0, 180))
        shadow_img.paste(shadow_solid, (shadow_blur, shadow_blur), mask=shadow_mask)
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(shadow_blur))
        final.alpha_composite(shadow_img, (x - shadow_blur + 5, y - shadow_blur + 20))
        
        # 2. Contact Floor Shadow (grounding the item)
        contact_w = int(new_w * 0.8)
        contact_h = int(new_h * 0.12)
        contact_shadow = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(contact_shadow)
        cx0 = int((new_w - contact_w) / 2)
        cy0 = new_h - contact_h + 10
        c_draw.ellipse([cx0, cy0, cx0 + contact_w, cy0 + contact_h], fill=(0, 0, 0, 200))
        contact_shadow = contact_shadow.filter(ImageFilter.GaussianBlur(12))
        final.alpha_composite(contact_shadow, (x, y))

        # 3. Soft reflection on premium floor
        refl = p_img.transpose(Image.FLIP_TOP_BOTTOM)
        refl_mask = Image.new("L", refl.size, 0)
        refl_draw = ImageDraw.Draw(refl_mask)
        for i in range(min(new_h, 250)):
            refl_draw.line([(0, i), (new_w, i)], fill=int(50 * (1 - i/250)))
        final.paste(refl, (x, y + new_h - 10), mask=refl_mask)
        
        # 4. Paste main Product
        final.alpha_composite(p_img, (x, y))

    # Save to the paths used in the web app
    final.save(os.path.join(OUTPUT_DIR, output_filename))
    print(f"Saved {output_filename} successfully!")

# Run Sets with Premium Navy Background and Catalog folder assets
# Set S
create_set_v3("Set S", [
    (PROD_1L, (260, 260), 0.72),
    (PROD_TEABAG, (480, 480), 0.68)
], "promo_set_s_lifestyle.png")

# Set M
create_set_v3("Set M", [
    (PROD_5L, (160, 230), 0.7),
    (PROD_1KG, (460, 330), 0.72),
    (PROD_TEABAG, (640, 520), 0.6)
], "promo_set_m_lifestyle.png")

# Set L
create_set_v3("Set L", [
    (PROD_5L, (80, 330), 0.58),
    (PROD_5L, (260, 330), 0.58),
    (PROD_6KG, (520, 230), 0.8), 
    (PROD_TEABAG, (180, 640), 0.44),
    (PROD_TEABAG, (380, 640), 0.44),
    (PROD_TEABAG, (580, 640), 0.44)
], "promo_set_l_lifestyle.png")
