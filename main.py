from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import re
import io

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OCR with pytesseract
    text = pytesseract.image_to_string(image)
    print("OCR text:", text)

    # Extract two numbers using regex
    numbers = re.findall(r'\d{8}', text.replace(" ", "").replace("x", "×"))

    if len(numbers) == 2:
        result = int(numbers[0]) * int(numbers[1])
        return JSONResponse({
            "answer": result,
            "email": "23f3002037@ds.study.iitm.ac.in"
        })
    else:
        return JSONResponse(
            {"error": "Could not extract two 8-digit numbers."}, status_code=400
        )
