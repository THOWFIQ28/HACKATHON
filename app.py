import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv", sep='\t')  # Ensure your CSV uses tabs
    return df

color_data = load_colors()
st.write("🎨 Loaded Color Data Sample:")
st.dataframe(color_data.head())

# Find closest color name
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            # ✅ Fixed Euclidean distance formula
            d = ((R - int(row['R']))**2 + (G - int(row['G']))**2 + (B - int(row['B']))**2) ** 0.5
            if d < min_dist:
                min_dist = d
                closest_color = row
        except Exception as e:
            st.write(f"Error reading row: {row} - {e}")
    
    if closest_color is not None:
        return closest_color
    else:
        return {
            'color_name': 'Unknown',
            'hex': '#000000'
        }

# Streamlit UI
st.title("🎨 Color Detection from Image (No OpenCV)")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("*Click on the image below to detect a color*")

    coords = streamlit_image_coordinates(image, key="click_image")

    if coords is not None:
        x, y = int(coords['x']), int(coords['y'])
        st.write(f"📍 Clicked Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if y < image_np.shape[0] and x < image_np.shape[1]:  # Ensure within bounds
            r, g, b = image_np[y, x]
            st.write(f"🎨 Clicked Pixel RGB: ({r}, {g}, {b})")

            color_info = get_color_name(r, g, b, color_data)
            hex_color = color_info['hex']
            color_name = color_info['color_name']

            st.markdown(f"""
            ### 🎯 Detected Color: {color_name}
            - RGB: ({r}, {g}, {b})
            - HEX: {hex_color}
            """)
            st.markdown(f"""
            <div style="width:100px; height:50px; background-color:{hex_color}; border:1px solid #000;"></div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Clicked outside image bounds.")
