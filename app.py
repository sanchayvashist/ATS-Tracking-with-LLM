import pytesseract
import os
import easyocr

import numpy as np
import google.generativeai as genai

from pdf2image import convert_from_path
from PIL import Image
from dotenv import load_dotenv


def get_gemini_response(model, resume_text, job_description):
    message = []

    print("Start Gen AI")

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

def straighen_image(image):
    text = pytesseract.image_to_osd(image)

    rotation_angle = 0
    for line in text.split("\n"):
        if line.startswith("Rotate:"):
            rotation_angle = int(line.split(":")[1].strip())

    return image.rotate(rotation_angle)



if __name__ == "__main__":
    load_dotenv()
    reader = easyocr.Reader(['en'])

    image_list = convert_from_path("Sanchay.pdf")
    key = os.environ["API_KEY"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    for image in image_list:
        image = straighen_image(image)
        data = np.array(image)
        results = reader.readtext(data, paragraph=True)
        resume_text = ""
        for result in results:
            resume_text = resume_text + " " + result[1]
    
    job_description = '''Key Responsibilities And Accountabilities
    Design, build, and measure complex ELT jobs to process disparate data sources and form a high integrity, high quality, clean data asset.
    Working on a range of projects including batch pipelines, data modeling, and data mart solutions you’ll be part of collaborative project teams working to implement robust data collection and processing pipelines to meet specific business need.
    Goals

    Design, build, and measure complex ELT jobs to process disparate data sources and form a high integrity, high quality, clean data asset.
    Executes and provides feedback for data modeling policies, procedure, processes, and standards.
    Assists with capturing and documenting system flow and other pertinent technical information about data, database design, and systems.
    Develop data quality standards and tools for ensuring accuracy.
    Work across departments to understand new data patterns.
    Translate high-level business requirements into technical specs.

    Required

    Bachelor’s degree in computer science or engineering.
    5+ years of experience with data analytics, data modeling, and database design.
    3+ years of coding and scripting (Python, Java, Pyspark) and design experience.
    3+ years of experience with Spark framework.
    Experience with ELT methodologies and tools.
    Experience with Vertica OR Teradata
    Expertise in tuning and troubleshooting SQL.
    Strong data integrity, analytical and multitasking skills.
    Excellent communication, problem solving, organizational and analytical skills.
    Able to work independently.'''

    print(get_gemini_response(model, resume_text, job_description))
        
        