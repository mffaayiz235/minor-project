import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
###########


##########
# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠ GOOGLE_API_KEY not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Set up Streamlit page
st.set_page_config(page_title="Food Nutrition Analyzer", page_icon="🍽")

# Sidebar for file upload
st.sidebar.title("Navigation")
st.sidebar.header("Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display main title
st.header("🍽 Food Nutrition Analyzer")

# Show the uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Define function to prepare image data
def input_image_setup(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        return None

# Define function to get AI response
def get_gemini_response(input_text, image_data):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([input_text, image_data[0]]) if image_data else None
    return response.text if response else "No valid image found for processing."

# AI prompt to extract complete food details
input_prompt = """
You are an expert nutritionist and food analyst. Analyze the food in the uploaded image and provide detailed information in the following structured format:

### *🍛 Food Name & Description*  
- Name of the food: [Provide food name]  
- Description: [Give a short background about the food]  

### *🥦 Nutritional Information*  
- Calories: [X kcal]  
- Protein: [X grams]  
- Carbohydrates: [X grams]  
- Fats: [X grams]  
- Fiber: [X grams]  
- Vitamins & Minerals: [List the key vitamins and minerals]  

### *✅ Advantages & ❌ Disadvantages*  
*✅ Advantages:*  
1. [Benefit 1]  
2. [Benefit 2]  
3. [Benefit 3]  

*❌ Disadvantages:*  
1. [Risk 1]  
2. [Risk 2]  
3. [Risk 3]  

### *👶 Recommended Age Group*  
- Suitable for: [Mention age group that can safely consume this food]  
- Not recommended for: [Mention if any group should avoid it]  

### *⭐ Health Rating*  
- Based on the nutritional value, this food gets a rating of *[X/10]* in terms of health benefits.  
"""

# Button to analyze food
if st.button("🍽 Analyse this Food"):
    if uploaded_file is None:
        st.warning("⚠ Please upload an image before clicking Analyse.")
    else:
        with st.spinner("Analyzing food... 🍕🥗🍎"):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
        st.success("✅ Analysis Complete!")
        st.subheader("📊 Food Analysis")
        st.write(response)