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

# Folder and files
assets_dir = r"c:\Users\Bon8\Downloads\open design\BioRevive_Website\assets"
images_to_process = [
    "product_liquid.png",
    "product_concentrated.png",
    "product_teabag.png"
]

for img_name in images_to_process:
    in_path = os.path.join(assets_dir, img_name)
    out_path = os.path.join(assets_dir, img_name.replace(".png", "_nobg.png"))
    
    if os.path.exists(in_path):
        remove_background(in_path, out_path)
    else:
        print(f"File not found: {in_path}")

print("Background removal completed!")
