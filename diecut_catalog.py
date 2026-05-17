import cv2
import numpy as np
import os

ASSETS_DIR = r"C:\BioRevive_Master\assets"
CATALOG_DIR = os.path.join(ASSETS_DIR, "catalog")
OUTPUT_DIR = ASSETS_DIR

def refine_mask(mask):
    # Smooth edges with morphological operations and blur
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    return mask

def diecut_product(img_name, bbox, thresh_fn, name):
    print(f"Die-cutting {name}...")
    img_path = os.path.join(CATALOG_DIR, img_name)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not load {img_name}")
        return
    
    # 1. Create a transparent canvas
    h, w, c = img.shape
    
    # 2. Extract bounding box of interest
    x1, y1, x2, y2 = bbox
    roi = img[y1:y2, x1:x2]
    
    # 3. Apply custom thresholding function
    mask_roi = thresh_fn(roi)
    
    # 4. Find the major contours in ROI
    contours, _ = cv2.findContours(mask_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create solid mask of the product inside the ROI
    solid_mask_roi = np.zeros(roi.shape[:2], dtype=np.uint8)
    if contours:
        # Keep contours that are reasonably large
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
        if large_contours:
            cv2.drawContours(solid_mask_roi, large_contours, -1, 255, -1)
        else:
            # Fallback to the single largest contour
            largest = max(contours, key=cv2.contourArea)
            cv2.drawContours(solid_mask_roi, [largest], -1, 255, -1)
            
    # Refine the solid mask inside ROI
    solid_mask_roi = refine_mask(solid_mask_roi)
    
    # Create full-size mask
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[y1:y2, x1:x2] = solid_mask_roi
    
    # Erase the floating text region on the right side of the teabag image
    if name == "teabag_with_6teabags":
        full_mask[180:780, 580:1000] = 0
    
    # 5. Anti-alias the mask edges with a soft Gaussian blur on the mask
    # We create a smooth alpha channel
    alpha = cv2.GaussianBlur(full_mask, (5, 5), 0)
    
    # 6. Build the transparent PNG image
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    
    # Crop the final output to tight product bounding box for neat arrangement
    x, y, w_box, h_box = cv2.boundingRect(full_mask)
    # Add a small padding
    pad = 10
    x_pad = max(0, x - pad)
    y_pad = max(0, y - pad)
    w_pad = min(w - x_pad, w_box + pad * 2)
    h_pad = min(h - y_pad, h_box + pad * 2)
    
    cropped = bgra[y_pad:y_pad+h_pad, x_pad:x_pad+w_pad]
    
    output_path = os.path.join(OUTPUT_DIR, f"ad_{name}_nobg.png")
    cv2.imwrite(output_path, cropped)
    print(f"Successfully saved {output_path} (Size: {cropped.shape[1]}x{cropped.shape[0]})")

# --- Threshold functions tailored for each product ---

def thresh_white_bottle(roi):
    # Bottles are very bright white compared to dark blue background
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY)
    return mask

def thresh_pouch_white(roi):
    # White pouch
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY)
    return mask

def thresh_bucket(roi):
    # White bucket
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    return mask

def thresh_teabag(roi):
    # Kraft paper is brownish (high Red, low Blue)
    # Background has very low Red (R < 35)
    r_channel = roi[:, :, 2]
    # Simple threshold on Red channel works beautifully for brown and white
    _, mask = cv2.threshold(r_channel, 45, 255, cv2.THRESH_BINARY)
    return mask

# --- Define crop regions and perform die-cutting ---

# 1. Liquid 1L
# catalog_liquid_1l.png - Bottle on the left
diecut_product(
    "catalog_liquid_1l.png",
    bbox=(110, 250, 520, 810),
    thresh_fn=thresh_white_bottle,
    name="liquid_1l"
)

# 2. Liquid 5L
# catalog_liquid_5l.png - Bottle in the center
diecut_product(
    "catalog_liquid_5l.png",
    bbox=(300, 160, 750, 850),
    thresh_fn=thresh_white_bottle,
    name="liquid_5l"
)

# 3. Premium 1KG Pouch
# catalog_pouch_1kg.png - Pouch in the center
diecut_product(
    "catalog_pouch_1kg.png",
    bbox=(420, 190, 880, 890),
    thresh_fn=thresh_pouch_white,
    name="pouch_white_1kg"
)

# 4. Premium 6KG Bucket (Commented out to keep the perfect git restored version)
# diecut_product(
#     "catalog_bucket_6kg.png",
#     bbox=(210, 180, 810, 830),
#     thresh_fn=thresh_bucket,
#     name="bucket_6kg"
# )

# 5. Teabag
# catalog_teabag.png - Pouch and teabags
diecut_product(
    "catalog_teabag.png",
    bbox=(40, 180, 980, 960), # Covers both pouch and the teabags at the bottom
    thresh_fn=thresh_teabag,
    name="teabag_with_6teabags"
)
