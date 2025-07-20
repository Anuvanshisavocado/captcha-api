from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image).strip()

        return JSONResponse(content={
            "answer": text,
            "email": "23f3002037@ds.study.iitm.ac.in"
        })

    except Exception as e:
        return JSONResponse(content={
            "error": str(e)
        }, status_code=500)
