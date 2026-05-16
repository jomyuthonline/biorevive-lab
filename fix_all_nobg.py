from rembg import remove
from PIL import Image
import os

ASSETS_DIR = r"C:\BioRevive_Master\assets"
files_to_fix = [
    "ad_liquid_1l.png",
    "ad_liquid_5l.png",
    "ad_pouch_white_1kg.png",
    "ad_bucket_6kg.png",
    "ad_teabag_with_6teabags.png"
]

for filename in files_to_fix:
    input_path = os.path.join(ASSETS_DIR, filename)
    output_path = os.path.join(ASSETS_DIR, filename.replace(".png", "_nobg.png"))
    
    if os.path.exists(input_path):
        print(f"Removing background from {filename}...")
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)
            with open(output_path, 'wb') as o:
                o.write(output_data)
        print(f"Saved {output_path}")
