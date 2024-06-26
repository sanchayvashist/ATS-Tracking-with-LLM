import pytesseract
import os
import easyocr

import streamlit as st
import numpy as np
import google.generativeai as genai

from pdf2image import convert_from_bytes
from PIL import Image
from dotenv import load_dotenv


# Get response from gemini 
def get_gemini_response(model, resume_text, job_description):
    message = []

    print("Generating ATS score using AI")

    replacements = {
        "resume_text" : resume_text,
        "job_description": job_description
    }

    with open("prompt.txt", "r") as file:
        prompt = file.read()
    
    for placeholder, value in replacements.items():
        prompt = prompt.replace(f'{{{placeholder}}}', value)

    message.append({"role": "user", "parts": [prompt]})

    response = model.generate_content(message)
    return response.text

# Funciton to Remove Rotation from image
def straighen_image(image):
    text = pytesseract.image_to_osd(image)

    rotation_angle = 0
    for line in text.split("\n"):
        if line.startswith("Rotate:"):
            rotation_angle = int(line.split(":")[1].strip())

    return image.rotate(rotation_angle)



if __name__ == "__main__":
    load_dotenv()

    st.title("Resume Shortlisting Using LLM")
    reader = easyocr.Reader(['en'])

    # Get Job discription for the role
    job_description = st.text_area("Job Descrition for the role")

    # Allow user to upload 
    uploaded_file = st.file_uploader("Upload pdf file")
    
    if uploaded_file and st.button("Generate Response"):
        # Convert pdf to image
        image_list = convert_from_bytes(uploaded_file.read())

        # Get api key from enviroment and intialize model
        key = os.environ["API_KEY"]
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Use OCR to extract text from image
        resume_text = ""
        for image in image_list:
            image = straighen_image(image)
            data = np.array(image)
            results = reader.readtext(data, paragraph=True)
            for result in results:
                resume_text = resume_text + " " + result[1]
        
        # Display response on Interface
        st.write(get_gemini_response(model, resume_text, job_description))
            
            