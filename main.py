import cv2
import numpy as np
from skimage import color
import pandas as pd
import os

# ===== Load image =====
image_path = r"image.jpg"  # Change to your image path
img = cv2.imread(image_path)

if img is None:
    print("Error: could not load image")
    exit()

# ===== Resize image =====
max_width = 900
max_height = 600

h, w = img.shape[:2]
scale = min(max_width / w, max_height / h)

if scale < 1:
    img = cv2.resize(img, (int(w * scale), int(h * scale)))

# ===== Copy for drawing =====
img_display = img.copy()

# ===== Save folder =====
save_folder = r"C:\Users\bilal\Downloads\New folder"
os.makedirs(save_folder, exist_ok=True)

data = []

# ===== Extraction function =====
def get_stable_rgb_and_accuracy(image, x, y, size=7):

    h, w, _ = image.shape

    x1 = max(0, x - size)
    x2 = min(w, x + size)
    y1 = max(0, y - size)
    y2 = min(h, y + size)

    region = image[y1:y2, x1:x2].copy()

    # Denoise region only
    region = cv2.fastNlMeansDenoisingColored(region, None, 10, 10, 7, 21)

    brightness = np.max(region, axis=2)
    mask = brightness < 240

    if np.any(mask):
        pixels = region[mask]
    else:
        pixels = region.reshape(-1, 3)

    b, g, r = np.median(pixels, axis=0)

    std = np.std(pixels, axis=0)
    accuracy = np.mean(std)

    return int(r), int(g), int(b), accuracy

# ===== RGB → LAB =====
def rgb_to_lab(r, g, b):
    rgb = np.array([[[r, g, b]]]) / 255.0
    lab = color.rgb2lab(rgb)
    return lab[0][0]

# ===== Mouse click =====
def click_event(event, x, y, flags, param):
    global img_display, data

    size = 7  # same as sampling size

    if event == cv2.EVENT_LBUTTONDOWN:

        r, g, b, acc = get_stable_rgb_and_accuracy(img, x, y, size)
        lab = rgb_to_lab(r, g, b)

        print("\nPoint:", (x, y))
        print(f"L = {lab[0]:.2f}, a = {lab[1]:.2f}, b = {lab[2]:.2f}")
        print(f"Accuracy: {acc:.2f}")

        data.append({
            "X": x,
            "Y": y,
            "L": round(lab[0], 2),
            "a": round(lab[1], 2),
            "b": round(lab[2], 2),
            "Accuracy": round(acc, 2)
        })

        # ✅ Draw sampling region box
        cv2.rectangle(img_display,
                      (x - size, y - size),
                      (x + size, y + size),
                      (0, 255, 0), 2)

        # ✅ Draw crosshair
        cv2.line(img_display, (x-10, y), (x+10, y), (0, 0, 255), 1)
        cv2.line(img_display, (x, y-10), (x, y+10), (0, 0, 255), 1)

        # ✅ Draw point circle
        cv2.circle(img_display, (x, y), 6, (0, 0, 255), -1)

        # ✅ Point number
        cv2.putText(img_display, str(len(data)), (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255), 2)

        cv2.imshow("Image", img_display)

# ===== Show image =====
cv2.imshow("Image", img_display)
cv2.setMouseCallback("Image", click_event)

print("Click on the image to measure LAB values")
print("Accuracy: low = stable, high = noisy")

cv2.waitKey(0)
cv2.destroyAllWindows()

# ===== Save results =====
if len(data) > 0:

    df = pd.DataFrame(data)

    excel_path = os.path.join(save_folder, "lab_results.xlsx")
    df.to_excel(excel_path, index=False)

    print("\n✅ Saved successfully:", excel_path)

else:
    print("\n⚠ No points selected")
