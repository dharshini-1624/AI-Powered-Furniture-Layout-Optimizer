import os
import numpy as np
import pandas as pd

# Ensure the Dataset folder exists
os.makedirs("Dataset", exist_ok=True)

# Define room dimensions (randomized within a range)
num_samples = 5000
room_widths = np.random.randint(8, 15, num_samples)
room_heights = np.random.randint(8, 15, num_samples)

# Define furniture types and their typical sizes
furniture_types = ["Bed", "Table", "Chair", "Sofa", "Wardrobe", "Desk", "Bookshelf", "Dining Table"]
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

# Generate furniture placements
data = []
for i in range(num_samples):
    room_w, room_h = room_widths[i], room_heights[i]
    num_furniture = np.random.randint(3, 6)

    furniture_placement = []
    for _ in range(num_furniture):
        f_type = np.random.choice(furniture_types)
        f_w, f_h = furniture_sizes[f_type]

        # Random placement within room
        x = np.random.randint(0, room_w - f_w + 1)
        y = np.random.randint(0, room_h - f_h + 1)

        furniture_placement.append(f"{f_type}({x},{y})")

    data.append([room_w, room_h, ";".join(furniture_placement)])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Room_Width", "Room_Height", "Furniture_Placement"])

# Save dataset in the correct folder
dataset_path = "C:/Users/saidh/Downloads/Furniture_Layout_Optimizer/AI_Furniture_Layout_Optimizer/Dataset/furniture_layout_dataset_5000.csv"
df.to_csv(dataset_path, index=False)

print(f"Dataset generated successfully and saved to {dataset_path}")

