from fastapi import FastAPI, Query
import joblib
import numpy as np
import pandas as pd
import random

# Load trained model
model = joblib.load("C:/Users/saidh/Downloads/Furniture_Layout_Optimizer/AI_Furniture_Layout_Optimizer/Model/furniture_placement_model_optimized.pkl")

app = FastAPI()

# Furniture types and sizes (width, height)
furniture_sizes = {
    "Bed": (4, 2),
    "Table": (2, 2),
    "Chair": (1, 1),
    "Sofa": (3, 2),
    "Wardrobe": (2, 3),
    "Desk": (3, 1),
    "Bookshelf": (2, 2),
    "Dining Table": (3, 3)
}

def parse_obstacles(obstacles_str):
    """Convert obstacles string 'x1,y1;x2,y2' into a list of (x, y) tuples."""
    return [(float(x), float(y)) for obs in obstacles_str.split(";") if len(obs.split(",")) == 2 for x, y in [obs.split(",")]]

def parse_furniture_constraints(furniture_str):
    """Convert furniture string 'Bed,Table,Chair' into a list of furniture items."""
    return [f.strip() for f in furniture_str.split(",") if f.strip() in furniture_sizes]

def is_valid_position(x, y, placed_items, room_w, room_h, min_spacing, obstacles, furniture_type):
    """Ensure furniture fits inside the room, does not overlap obstacles, and maintains spacing."""

    fw, fh = furniture_sizes.get(furniture_type, (2, 2))  # Get furniture size

    # Ensure furniture stays inside the room
    if x + fw > room_w or y + fh > room_h:
        return False  

    # Ensure furniture isn't placed too close to walls (10% margin)
    margin = max(room_w, room_h) * 0.1
    if x < margin or y < margin or x + fw > room_w - margin or y + fh > room_h - margin:
        return False  

    # Ensure no overlap with obstacles
    for ox, oy in obstacles:
        if ((x - ox) ** 2 + (y - oy) ** 2) ** 0.5 < min_spacing:
            return False  

    # Ensure spacing from already placed furniture
    for item in placed_items:
        if len(item) == 4:  # Expected format (px, py, pw, ph)
            px, py, pw, ph = item
        elif len(item) == 2:  # If the entry only has (px, py), assume default size
            px, py = item
            pw, ph = 2, 2  # Default small size if not provided
        else:
            continue  # Skip incorrectly formatted entries

        if ((x - px) ** 2 + (y - py) ** 2) ** 0.5 < min_spacing:
            return False  

    return True

@app.get("/predict_placement/")
def predict_placement(
    room_width: int, 
    room_height: int, 
    furniture_constraints: str = Query("", description="Furniture types as 'Bed,Table,Chair'"), 
    obstacles: str = Query("", description="Obstacles as 'x1,y1;x2,y2' (e.g., '6,0;0,9')")
):
    """Predicts optimized furniture placement based on room size, furniture constraints, and obstacles."""
    
    obstacles_list = parse_obstacles(obstacles)
    furniture_list = parse_furniture_constraints(furniture_constraints)

    # Get AI-generated base placement
    input_features = pd.DataFrame([[room_width, room_height]], columns=["Room_Width", "Room_Height"])
    base_x, base_y = model.predict(input_features)[0]

    base_x, base_y = round(base_x, 2), round(base_y, 2)
    min_spacing = max(room_width, room_height) * 0.2  
    placements = []

    for furniture_type in furniture_list:
        attempts = 0
        while attempts < 200:  
            x_offset, y_offset = random.uniform(-3, 3), random.uniform(-3, 3)
            new_x, new_y = min(max(base_x + x_offset, 0), room_width), min(max(base_y + y_offset, 0), room_height)

            if is_valid_position(new_x, new_y, placements, room_width, room_height, min_spacing, obstacles_list, furniture_type):
                fw, fh = furniture_sizes.get(furniture_type, (2, 2))
                placements.append([furniture_type, round(new_x, 2), round(new_y, 2), fw, fh])
                break  
            attempts += 1  

    return {
        "room_width": room_width,
        "room_height": room_height,
        "furniture_constraints": furniture_list,
        "obstacles": obstacles_list,
        "predicted_positions": placements
    }