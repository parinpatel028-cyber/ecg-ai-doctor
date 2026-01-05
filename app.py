import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SECURITY NOTE ---
# In the box below, paste the key you got from Google inside the quotes
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

st.set_page_config(page_title="ECG Rapid Tutor", layout="centered")

# --- APP DESIGN ---
st.title("🫀 ECG Rapid Interpretation")
st.write("Upload an ECG photo. The AI will interpret it and teach you the findings.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Take a photo of the ECG...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Show the image
    image = Image.open(uploaded_file)
    st.image(image, caption='ECG Image', use_column_width=True)

    if st.button("INTERPRET NOW"):
        with st.spinner('Analyzing rhythm strip...'):
            try:
                # This is the Brain
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # This is what we ask the AI
                prompt = """
                Act as a senior cardiologist professor. Analyze this ECG image carefully.
                Output the result in this exact format:
                
                1. **Rhythm Analysis:** (Regular/Irregular, Rate, P-waves)
                2. **Morphology:** (ST changes, QRS width, T-wave abnormalities)
                3. **Primary Interpretation:** (What is the likely diagnosis?)
                4. **Learning Point:** (Explain specifically WHY you made this diagnosis based on the visual evidence. Teach me.)
                
                DISCLAIMER: State clearly this is for educational use only.
                """
                
                response = model.generate_content([prompt, image])
                
                # Show result
                st.success("Analysis Ready!")
                st.markdown(response.text)
                st.info("💡 Note: Always correlate with patient clinical status.")
                
            except Exception as e:
                st.error(f"Error: {e}. Please try again.")
