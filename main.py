from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import pytesseract
from PIL import Image

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    # Poți adăuga pre-procesare dacă vrei (binarizare, crop etc.)
    plate_number = pytesseract.image_to_string(image, config='--psm 7')  # PSM 7: line of text
    plate_number = ''.join(filter(str.isalnum, plate_number))  # Curăță outputul, doar litere/cifre
    return JSONResponse(content={"plate": plate_number})
