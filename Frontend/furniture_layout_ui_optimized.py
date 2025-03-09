import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("AI Furniture Layout Optimizer")

room_width = st.number_input("Room Width", min_value=5, max_value=20, value=12)
room_height = st.number_input("Room Height", min_value=5, max_value=20, value=10)
furniture_constraints = st.text_input("Furniture Constraints (comma-separated)", "Bed,Table,Chair")
obstacles = st.text_input("Obstacles (optional, format: x1,y1;x2,y2)", "")

if st.button("Generate Layout"):
    url = f"http://127.0.0.1:8080/predict_placement/?room_width={room_width}&room_height={room_height}&furniture_constraints={furniture_constraints}&obstacles={obstacles}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.json(data)

        # Extract room details and predicted positions
        room_w = data["room_width"]
        room_h = data["room_height"]
        furniture_positions = data["predicted_positions"]

        # Visualization
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.set_xlim(0, room_w)
        ax.set_ylim(0, room_h)
        ax.set_xlabel("Room Width")
        ax.set_ylabel("Room Height")

        # Draw furniture
        for item in furniture_positions:
            name, x, y, fw, fh = item
            rect = plt.Rectangle((x, y), fw, fh, linewidth=2, edgecolor='blue', facecolor='lightblue', label=name)
            ax.add_patch(rect)
            ax.text(x + fw / 2, y + fh / 2, name, fontsize=8, ha='center', va='center')

        plt.title("Optimized Furniture Layout")
        plt.grid(True)
        st.pyplot(fig)
    else:
        st.error("Error: Could not retrieve data. Make sure the API is running.")