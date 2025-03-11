from fastapi import FastAPI, Query
import joblib
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

def check_collision(x, y, fw, fh, placed_items):
    """Check if new furniture overlaps with already placed items."""
    for item in placed_items:
        if len(item) == 5:  # Ensure correct unpacking
            px, py, pw, ph = item[1], item[2], item[3], item[4]
            if not (x + fw <= px or px + pw <= x or y + fh <= py or py + ph <= y):
                return True  # Overlapping detected
    return False

def is_valid_position(x, y, fw, fh, placed_items, room_w, room_h, obstacles):
    """Ensure furniture fits inside the room, does not overlap obstacles, and maintains spacing."""
    # Ensure furniture stays inside the room
    if x + fw > room_w or y + fh > room_h:
        return False  

    # Ensure no overlap with obstacles
    for ox, oy in obstacles:
        if ((x - ox) ** 2 + (y - oy) ** 2) ** 0.5 < 1:
            return False  

    # Ensure spacing from already placed furniture
    if check_collision(x, y, fw, fh, placed_items):
        return False

    return True

@app.get("/predict_placement/")
def predict_placement(
    room_width: int, 
    room_height: int, 
    furniture_constraints: str = Query("", description="Furniture types as 'Bed,Table,Chair'"), 
    obstacles: str = Query("", description="Obstacles as 'x1,y1;x2,y2' (e.g., '6,0;0,9')")
):
    obstacles_list = parse_obstacles(obstacles)
    furniture_list = parse_furniture_constraints(furniture_constraints)

    # Check if all selected furniture fits in the available room space
    available_area = room_width * room_height
    total_furniture_area = sum([furniture_sizes[f][0] * furniture_sizes[f][1] for f in furniture_list])

    if total_furniture_area > available_area * 0.7:
        return {"error": "The selected furniture exceeds the available space."}

    # Place furniture in the room dynamically
    placed_items = []
    for furniture in furniture_list:
        fw, fh = furniture_sizes.get(furniture, (2, 2))
        placed = False
        attempts = 0
        
        while not placed and attempts < 200:  # Try 200 times to place furniture
            x = random.uniform(0, room_width - fw)
            y = random.uniform(0, room_height - fh)
            if is_valid_position(x, y, fw, fh, placed_items, room_width, room_height, obstacles_list):
                placed_items.append([furniture, round(x, 2), round(y, 2), fw, fh])
                placed = True
            attempts += 1
        
        if not placed:
            return {"error": f"Unable to place {furniture} due to space constraints."}

    return {
        "room_width": room_width,
        "room_height": room_height,
        "furniture_constraints": furniture_list,
        "obstacles": obstacles_list,
        "predicted_positions": placed_items
    }