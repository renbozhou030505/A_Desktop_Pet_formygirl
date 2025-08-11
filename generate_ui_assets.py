# generate_ui_assets.py (Upgraded for 9-Patch Scaling)
import os
from PIL import Image, ImageDraw

ASSET_DIR = "assets"
IMAGE_NAME = "bubble_background_template.png" # Use a new name to avoid confusion

# --- Configuration for a scalable template ---
# We define the size of the corners and the tail. The center part will be stretched.
CORNER_RADIUS = 12
TAIL_HEIGHT = 8
TAIL_WIDTH = 12
BORDER_WIDTH = 2
# The canvas size is now calculated based on the core components
CANVAS_WIDTH = CORNER_RADIUS * 2 + TAIL_WIDTH # A width that can contain corners and tail
CANVAS_HEIGHT = CORNER_RADIUS * 2 + TAIL_HEIGHT

BG_COLOR = "#FFFFFF"
BORDER_COLOR = "#4a4a4a"

def generate_bubble_template():
    """
    Generates a small, clean bubble template for use with CSS border-image.
    This image is meant to be sliced and stretched, not used as-is.
    """
    if not os.path.exists(ASSET_DIR):
        os.makedirs(ASSET_DIR)

    # Create a transparent canvas
    img = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define the rectangle for the main body of the bubble (without the tail)
    bubble_rect = (0, 0, CANVAS_WIDTH - 1, CANVAS_HEIGHT - TAIL_HEIGHT - 1)

    # Define the tail polygon, pointing downwards from the center
    tail_x_center = CANVAS_WIDTH / 2
    tail_points = [
        (tail_x_center - TAIL_WIDTH / 2, bubble_rect[3]),
        (tail_x_center, bubble_rect[3] + TAIL_HEIGHT),
        (tail_x_center + TAIL_WIDTH / 2, bubble_rect[3])
    ]

    # Draw the shape: rounded rectangle and tail
    draw.rounded_rectangle(bubble_rect, radius=CORNER_RADIUS, fill=BG_COLOR, outline=BORDER_COLOR, width=BORDER_WIDTH)
    draw.polygon(tail_points, fill=BG_COLOR)
    # Draw the tail border lines manually
    draw.line([tail_points[0], tail_points[1]], fill=BORDER_COLOR, width=BORDER_WIDTH)
    draw.line([tail_points[1], tail_points[2]], fill=BORDER_COLOR, width=BORDER_WIDTH)

    # Save the final template image
    output_path = os.path.join(ASSET_DIR, IMAGE_NAME)
    img.save(output_path)
    print(f"🎨 可伸缩的气泡模板已生成: {output_path}")

if __name__ == "__main__":
    generate_bubble_template()