from PIL import Image, ImageDraw, ImageFilter
import os

# Paths
ASSETS_DIR = r"C:\BioRevive_Master\assets"
CATALOG_DIR = os.path.join(ASSETS_DIR, "catalog")
OUTPUT_DIR = ASSETS_DIR

# Products (Verified Nobg versions)
PROD_1L = os.path.join(ASSETS_DIR, "ad_liquid_1l_nobg.png")
PROD_5L = os.path.join(ASSETS_DIR, "ad_liquid_5l_nobg.png")
PROD_1KG = os.path.join(ASSETS_DIR, "ad_pouch_white_1kg_nobg.png")
PROD_6KG = os.path.join(ASSETS_DIR, "ad_bucket_6kg_nobg.png")
PROD_TEABAG = os.path.join(ASSETS_DIR, "ad_teabag_with_6teabags_nobg.png")

def create_set_v3(name, products, output_filename):
    print(f"Creating Premium Catalog {name}...")
    w, h = 1024, 1024
    # Create Premium Navy Gradient Background
    final = Image.new("RGBA", (w, h), (14, 28, 48, 255))
    draw = ImageDraw.Draw(final)
    
    # Draw subtle gradient
    for y in range(h):
        r = int(14 + (20 - 14) * (y / h))
        g = int(28 + (40 - 28) * (y / h))
        b = int(48 + (65 - 48) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Add Gold Accent Lines (Vibrant & Clean)
    gold = (197, 160, 89, 150)
    draw.line([(0, h*0.2), (w, h*0.1)], fill=gold, width=1)
    draw.line([(w*0.7, 0), (w, h*0.3)], fill=gold, width=1)
    
    # Add a soft floor glow
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([w*0.1, h*0.7, w*0.9, h*0.9], fill=(255, 255, 255, 10))
    final.alpha_composite(glow.filter(ImageFilter.GaussianBlur(30)))

    # Sort products
    products.sort(key=lambda x: x[1][1])
    
    for p_path, pos, scale in products:
        p_img = Image.open(p_path).convert("RGBA")
        new_w = int(p_img.width * scale)
        new_h = int(p_img.height * scale)
        p_img = p_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        x, y = pos
        
        # 1. Realistic Soft Drop Shadow
        shadow_blur = 30
        shadow_img = Image.new("RGBA", (new_w + shadow_blur*2, new_h + shadow_blur*2), (0, 0, 0, 0))
        shadow_mask = p_img.split()[3]
        shadow_solid = Image.new("RGBA", p_img.size, (0, 0, 0, 160))
        shadow_img.paste(shadow_solid, (shadow_blur, shadow_blur), mask=shadow_mask)
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(shadow_blur))
        final.alpha_composite(shadow_img, (x - shadow_blur + 5, y - shadow_blur + 15))

        # 2. Floor Reflection (Faded)
        refl = p_img.transpose(Image.FLIP_TOP_BOTTOM)
        refl_mask = Image.new("L", refl.size, 0)
        refl_draw = ImageDraw.Draw(refl_mask)
        for i in range(min(new_h, 200)):
            refl_draw.line([(0, i), (new_w, i)], fill=int(40 * (1 - i/200)))
        final.paste(refl, (x, y + new_h - 10), mask=refl_mask)
        
        # 3. Paste Product
        final.alpha_composite(p_img, (x, y))

    final.save(os.path.join(OUTPUT_DIR, output_filename))
    print(f"Saved {output_filename}")

# Run Sets with V3
# Set S
create_set_v3("Set S", [
    (PROD_1L, (280, 280), 0.7),
    (PROD_TEABAG, (520, 480), 0.6)
], "promo_set_s_new.png")

# Set M
create_set_v3("Set M", [
    (PROD_5L, (180, 250), 0.7),
    (PROD_1KG, (480, 350), 0.7),
    (PROD_TEABAG, (650, 520), 0.58)
], "promo_set_m_new.png")

# Set L
create_set_v3("Set L", [
    (PROD_5L, (80, 350), 0.58),
    (PROD_5L, (280, 350), 0.58),
    (PROD_6KG, (520, 250), 0.8), 
    (PROD_TEABAG, (220, 650), 0.4),
    (PROD_TEABAG, (420, 650), 0.4),
    (PROD_TEABAG, (620, 650), 0.4)
], "promo_set_l_new.png")
