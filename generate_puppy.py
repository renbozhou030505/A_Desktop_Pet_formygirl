# generate_puppy.py
import os, math, json, shutil
from PIL import Image, ImageDraw

# Config
PET_NAME = "puppy_classic"
CANVAS_SIZE = (60, 60)
OUTPUT_DIR = os.path.join("pets", PET_NAME, "pet_images")
CONFIG_PATH = os.path.join("pets", PET_NAME, "pet_config.json")
COLORS = {"body": "#c68642", "ear": "#8d5524", "eye": "#000000", "nose": "#333333", "tail": "#8d5524"}

KEYFRAMES = {
    "standing": {'frames_between': 10, 'params': {'body_y_offset': [0, -2, 0], 'tail_angle': [-25, -35, -25], 'ear_y_offset': [0, 1, 0]}},
    "running": {'frames_between': 5, 'params': {'body_y_offset': [0, -4, 0, 4, 0], 'tail_angle': [-20, -50, -20, 10, -20], 'ear_y_offset': [0, 5, 0, 3, 0]}},
    "sleeping": {'frames_between': 20, 'params': {'is_sleeping': [True, True], 'body_y_offset': [8, 9, 8], 'body_squash': [1.2, 1.2, 1.2]}},
    "interacting": {'frames_between': 4, 'params': {'tail_angle': [-20, -60, 20, -60, -20], 'ear_y_offset': [0, 2, -2, 2, 0]}}
}

def lerp(a, b, t): return a * (1 - t) + b * t

def draw_puppy(p): # p for params
    img = Image.new('RGBA', CANVAS_SIZE, (0, 0, 0, 0)); draw = ImageDraw.Draw(img)
    y_off, tail_a, ear_y = p.get('body_y_offset', 0), p.get('tail_angle', -25), p.get('ear_y_offset', 0)
    sleeping, squash = p.get('is_sleeping', False), p.get('body_squash', 1.0)
    
    body_w, body_h = 28 * squash, 22 / squash; body_x, body_y = (CANVAS_SIZE[0] - body_w) / 2, 20 + y_off
    draw.ellipse([body_x, body_y, body_x + body_w, body_y + body_h], fill=COLORS['body'])
    head_w, head_h = 24, 24; head_x, head_y = body_x + body_w - 22, body_y - 12
    draw.ellipse([head_x, head_y, head_x + head_w, head_y + head_h], fill=COLORS['body'])
    nose_r = 2; nose_x, nose_y = head_x + head_w - 4, head_y + head_h / 2
    draw.ellipse([nose_x-nose_r, nose_y-nose_r, nose_x+nose_r, nose_y+nose_r], fill=COLORS['nose'])
    ear_w, ear_h = 10, 14; ear_x, ear_y = head_x + 5, head_y + ear_y
    draw.ellipse([ear_x, ear_y, ear_x + ear_w, ear_y + ear_h], fill=COLORS['ear'])
    eye_r = 1.5; eye_x, eye_y = head_x + 12, head_y + 10
    if sleeping: draw.arc([eye_x - 3, eye_y - 2, eye_x + 3, eye_y + 2], 200, 340, fill=COLORS['eye'], width=1)
    else: draw.ellipse([eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r], fill=COLORS['eye'])
    tail_len, tail_rad = 12, math.radians(tail_a); sx, sy = body_x + 5, body_y + body_h / 2
    ex, ey = sx - tail_len * math.cos(tail_rad), sy - tail_len * math.sin(tail_rad)
    draw.line([sx, sy, ex, ey], fill=COLORS['tail'], width=4, joint="curve")
    return img

if __name__ == "__main__":
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print(f"Generating assets for '{PET_NAME}'...")
    
    pet_cfg = {"name": "Classic Puppy", "author": "You", "version": "1.0", "size": list(CANVAS_SIZE), "animation_interval": 33, "states": []}
    total_frames = 0
    
    for state, data in KEYFRAMES.items():
        print(f"Rendering state: {state}")
        pet_cfg["states"].append({"name": state, "loop": True, "duration": 2000})
        params, num_frames = data['params'], data['frames_between']
        keyframe_count = len(next(iter(params.values())))
        
        frame_idx = 0
        for i in range(keyframe_count - 1):
            for j in range(num_frames):
                t = j / num_frames; current_params = {}
                for name, values in params.items():
                    current_params[name] = lerp(values[i], values[i+1], t)
                
                image = draw_puppy(current_params)
                image.save(f"{OUTPUT_DIR}/{state}_{frame_idx}.png")
                frame_idx += 1
        total_frames += frame_idx
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: json.dump(pet_cfg, f, indent=4)
    print(f"\nGeneration complete. {total_frames} frames created.")