# generate_ui_assets.py (Artist Edition)
import os
from PIL import Image, ImageDraw, ImageFilter

ASSET_DIR = "assets"
IMAGE_NAME = "bubble_background.png"
CANVAS_SIZE = (80, 60); CORNER_RADIUS = 15; TAIL_HEIGHT = 12; TAIL_WIDTH = 16
SHADOW_COLOR = (0, 0, 0, 40); SHADOW_OFFSET = (1, 1); SHADOW_BLUR = 3
BG_COLOR = "#FFFFFF"; BORDER_COLOR = "#4a4a4a"; BORDER_WIDTH = 2

def generate_bubble_image():
    if not os.path.exists(ASSET_DIR): os.makedirs(ASSET_DIR)
    img = Image.new('RGBA', (CANVAS_SIZE[0] + SHADOW_BLUR*2, CANVAS_SIZE[1] + SHADOW_BLUR*2), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    bubble_rect = (SHADOW_BLUR, SHADOW_BLUR, SHADOW_BLUR + CANVAS_SIZE[0] - 1, SHADOW_BLUR + CANVAS_SIZE[1] - TAIL_HEIGHT - 1)
    tail_points = [
        (bubble_rect[0] + CORNER_RADIUS, bubble_rect[3]),
        (bubble_rect[0] + CORNER_RADIUS + TAIL_WIDTH / 2, bubble_rect[3] + TAIL_HEIGHT),
        (bubble_rect[0] + CORNER_RADIUS + TAIL_WIDTH, bubble_rect[3])
    ]
    mask = Image.new('L', img.size, 0); mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(bubble_rect, radius=CORNER_RADIUS, fill=255); mask_draw.polygon(tail_points, fill=255)
    shadow_layer = mask.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    img.paste(Image.new('RGBA', img.size, SHADOW_COLOR), (SHADOW_OFFSET[0], SHADOW_OFFSET[1]), mask=shadow_layer)
    draw.rounded_rectangle(bubble_rect, fill=BG_COLOR, outline=BORDER_COLOR, width=BORDER_WIDTH)
    draw.polygon(tail_points, fill=BG_COLOR); draw.line([tail_points[0], tail_points[2]], fill=BORDER_COLOR, width=BORDER_WIDTH)
    output_path = os.path.join(ASSET_DIR, IMAGE_NAME); img.save(output_path)
    print(f"🎨 终极艺术气泡背景已生成: {output_path}")

if __name__ == "__main__":
    generate_bubble_image()