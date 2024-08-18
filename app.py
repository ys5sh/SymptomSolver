# importing Module
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key


# Configure API key
genai.configure(api_key=api_key)

system_prompt="""

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions.

Please provide me an output response with these 4 headings Detailed Analysis, Finding Repport, Recommendation and Next steps, Treatment Suggestion

"""

# Create the model
generation_config = {
  "temperature": 0.95,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# config model
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

#Page Configiration

st.set_page_config(page_title="Symptom Solver" , page_icon="icon.png")

st.markdown("""
<style>
  footer {
    visibility: hidden;
  }
  #deploy-btn {
        visibility: hidden;
    }
  #MainMenu {
    visibility: hidden;
  }
  header {
    visibility: hidden;
  }
  
</style>
""", unsafe_allow_html=True)

#logo
st.image("logo.png", width=200); 

#set the title
st.title("Not feeling well? Snap a pic of your symptom & injury and we'll help.")
st.image("cover.png", use_column_width=True)
#set the description
st.subheader("AI Doctor : Your Personal Health Advisor")

st.write("Experience cutting-edge healthcare with our AI Doctor. Accurately analyze symptoms, receive detailed reports outlining potential health issues, and get personalized treatment recommendations. Our AI offers clear next steps and empowers you to make informed decisions about your health. From initial assessment to ongoing care, we're here to support you.")
# Create a list of image URLs and captions

st.write("Upload the medical image for Analysis, sample Image : ")
st.image("sample.jpg", width= 220)


#upload
uploaded_file = st.file_uploader ("Upload Image here : ",type = ["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, width= 300, caption= "uploaded Medical Image")
submit_button = st.button("Generate the Analysis")

if submit_button:
    image_data = uploaded_file.getvalue()
    image_parts = [{
    "data" : image_data, "mime_type" : "image/jpeg"
    },]

    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    st.title("Here is the analysis based on your Image")
    response = model.generate_content(prompt_parts)

    st.write(response.text)

st.write("Developed by Yash and Yashika ✨")
