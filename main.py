from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pytesseract import image_to_string
from PIL import Image
import io
import re

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read image bytes
        image_data = await file.read()
        
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("L")  # Convert to grayscale if needed

        # OCR to extract text
        text = image_to_string(image)
        print("OCR Result:", text)

        # Extract two 8-digit numbers and operator
        match = re.search(r"(\d{8})\s*[\*xX×]\s*(\d{8})", text.replace(" ", ""))
        if not match:
            return {
                "error": "Unable to extract two 8-digit numbers from image",
                "text": text
            }

        num1 = int(match.group(1))
        num2 = int(match.group(2))
        result = num1 * num2

        # Return result and email
        return {
            "answer": result,
            "email": "23f3002037@ds.study.iitm.ac.in"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
