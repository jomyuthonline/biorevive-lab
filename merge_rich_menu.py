from PIL import Image

def process_rich_menu():
    # Paths
    logo_path = r'c:\Users\Bon8\Downloads\open design\BioRevive_Website\assets\logo.png'
    bg_path = r'C:\Users\Bon8\.gemini\antigravity\brain\4feb6c0c-a6ff-49d7-935e-a530609717d8\biorevive_rich_menu_v2_template_1778417466148.png'
    output_path = r'C:\Users\Bon8\.gemini\antigravity\brain\4feb6c0c-a6ff-49d7-935e-a530609717d8\biorevive_rich_menu_final_pro.png'

    # Open logo and remove white background
    logo = Image.open(logo_path).convert('RGBA')
    data = logo.getdata()
    
    new_data = []
    for item in data:
        # If the pixel is very white, make it transparent
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    logo.putdata(new_data)

    # Open background template
    background = Image.open(bg_path).convert('RGBA')
    bg_w, bg_h = background.size

    # Resize logo
    scale = 0.38
    new_w = int(bg_w * scale)
    new_h = int(logo.size[1] * (new_w / logo.size[0]))
    logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Calculate position
    pos_x = (bg_w - new_w) // 2
    pos_y = int(bg_h * 0.10) # Positioned at the top

    # Paste logo
    background.paste(logo, (pos_x, pos_y), logo)

    # Save final result
    background.save(output_path)
    print(f"Final Rich Menu saved to: {output_path}")

if __name__ == "__main__":
    process_rich_menu()
