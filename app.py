import pytesseract

from pdf2image import convert_from_path
from PIL import Image

def straighen_image(image):
    text = pytesseract.image_to_osd(image)

    rotation_angle = 0
    for line in text.split('\n'):
        if line.startswith('Rotate:'):
            rotation_angle = int(line.split(':')[1].strip())

    
    return image.rotate(rotation_angle)


if __name__ == "__main__":
    image_list = convert_from_path("Sanchay.pdf")
    
    for image in image_list:
        image = straighen_image(image)
        print(image)