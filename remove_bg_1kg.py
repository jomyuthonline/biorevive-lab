import os
from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    print(f"Processing: {input_path}")
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Saved transparent image to: {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

assets_dir = r"c:\BioRevive_Master\assets"
in_path = os.path.join(assets_dir, "product_soil1kg.jpg")
out_path = os.path.join(assets_dir, "product_soil1kg_nobg.png")

if os.path.exists(in_path):
    remove_background(in_path, out_path)
else:
    print(f"File not found: {in_path}")
