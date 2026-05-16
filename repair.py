from PIL import Image, ImageDraw
import os

def repair_image():
    input_path = 'assets/fb_post_teabag.png'
    output_path = r'C:\Users\Bon8\.gemini\antigravity\brain\a7b8dbe2-4d34-4b7b-9738-990c64564a71\repaired_teabag.png'
    
    try:
        img = Image.open(input_path).convert("RGBA")
        w, h = img.size
        
        # 1. Remove the blue stripe (approximate coordinates based on standard 1350x1350)
        # The stripe is a horizontal line across the middle of the bag.
        # Let's say it's between y=650 and y=750.
        # We can take a slice from y=600-640 and stretch/paste it.
        # However, it might look obvious.
        # Better: Crop a healthy part of the bag and paste it.
        
        # Let's try to just show the user a "Cleaned" version by masking.
        # Actually, if I can't do it perfectly, I should ask if they have a version without the flare.
        
        # 2. Mask the 7th teabag.
        # Teabags are at the bottom right.
        # We can draw a black polygon over the extra teabags before rembg.
        
        draw = ImageDraw.Draw(img)
        # Mask out the far right teabags to leave only 6
        # Assuming teabags are roughly in a row/cluster at the bottom
        # This is very hard without seeing exact coordinates.
        
        # Let's try to just crop the bag first and see if I can fix the stripe.
        bag_area = img.crop((400, 350, 950, 1100)) # Approximate bag area
        
        # Attempt to "Heal" the stripe by blending.
        # Let's just save this for now to show the user my progress.
        bag_area.save(output_path)
        print("Draft repair saved.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    repair_image()
