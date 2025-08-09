# utils/asset_loader.py
import os
import json
from PyQt6.QtGui import QPixmap

PETS_DIR = "pets"

def load_pet(pet_name):
    pet_path = os.path.join(PETS_DIR, pet_name)
    if not os.path.isdir(pet_path):
        raise FileNotFoundError(f"Pet package not found at: {pet_path}")
    
    config_path = os.path.join(pet_path, "pet_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    images_path = os.path.join(pet_path, "pet_images")
    animations = {}
    
    for state_info in config.get("states", []):
        state_name = state_info['name']
        frames = []
        i = 0
        while True:
            frame_path = os.path.join(images_path, f"{state_name}_{i}.png")
            if os.path.exists(frame_path):
                frames.append(QPixmap(frame_path))
                i += 1
            else:
                break
        if frames:
            animations[state_name] = frames

    return config, animations