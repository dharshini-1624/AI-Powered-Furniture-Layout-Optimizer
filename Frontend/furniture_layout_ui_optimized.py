import streamlit as st
import requests
import matplotlib.pyplot as plt

# Furniture sizes as (width, height)
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

st.title("AI Furniture Layout Optimizer")

# User input for room dimensions
room_width = st.number_input("Room Width", min_value=5, max_value=20, value=8)
room_height = st.number_input("Room Height", min_value=5, max_value=20, value=6)

# Room area calculation
room_area = room_width * room_height
max_furniture_area = room_area * 0.7  # Allow only 70% of the room's area for furniture
remaining_area = max_furniture_area

st.write(f"Room Area: {room_area} sq units")
st.write(f"Max Furniture Area Allowed: {max_furniture_area} sq units")

# User selects furniture
furniture_constraints = st.multiselect(
    "Select Furniture (based on available space)",
    options=list(furniture_sizes.keys())
)

# User input for obstacles
obstacles_input = st.text_input(
    "Enter Obstacles (optional, format: x1,y1;x2,y2; ...)",
    value=""
)

# Parse the obstacle input
obstacles_list = []
if obstacles_input:
    obstacles_list = obstacles_input.split(";")
    obstacles_list = [(float(x), float(y)) for x, y in (obs.split(",") for obs in obstacles_list)]

# Calculate the total area of selected furniture
total_furniture_area = sum([furniture_sizes[f][0] * furniture_sizes[f][1] for f in furniture_constraints])

if total_furniture_area > remaining_area:
    st.warning("The selected furniture exceeds the available space. Please adjust your selection.")

if st.button("Generate Layout"):
    if total_furniture_area <= remaining_area:
        url = f"http://127.0.0.1:8080/predict_placement/?room_width={room_width}&room_height={room_height}&furniture_constraints={','.join(furniture_constraints)}&obstacles={obstacles_input}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(data["error"])
            else:
                room_w = data["room_width"]
                room_h = data["room_height"]
                furniture_positions = data["predicted_positions"]

                # Displaying the furniture placement coordinates first
                st.write("Furniture Placement Coordinates:")
                for item in furniture_positions:
                    name, x, y, fw, fh = item
                    st.write(f"{name}: ({round(x, 2)}, {round(y, 2)})")

                # Visualization of the furniture layout
                fig, ax = plt.subplots(figsize=(6, 5))
                ax.set_xlim(0, room_w)
                ax.set_ylim(0, room_h)
                ax.set_xlabel("Room Width")
                ax.set_ylabel("Room Height")

                colors = ["blue", "red", "green", "purple", "orange", "cyan", "pink", "yellow"]
                color_map = {}

                # Loop through furniture and plot each piece with coordinates
                for i, item in enumerate(furniture_positions):
                    name, x, y, fw, fh = item
                    if name not in color_map:
                        color_map[name] = colors[i % len(colors)]
                    rect = plt.Rectangle((x, y), fw, fh, linewidth=2, edgecolor='black', facecolor=color_map[name], alpha=0.6)
                    ax.add_patch(rect)
                    ax.text(x + fw / 2, y + fh / 2, f"{name}\n({round(x, 2)}, {round(y, 2)})", fontsize=8, ha='center', va='center')

                plt.title("Optimized Furniture Layout")
                plt.grid(True)
                st.pyplot(fig)
        else:
            st.error("Error: Could not retrieve data. Make sure the API is running.")
    else:
        st.error("Selected furniture exceeds available space in the room. Please remove some items.")
