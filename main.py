from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import easyocr
from PIL import Image
import numpy as np

app = FastAPI()
reader = easyocr.Reader(['en', 'ro'], gpu=False)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    np_img = np.array(image)
    results = reader.readtext(np_img)
    plates = [text for _, text, _ in results]
    plate_number = max(plates, key=len) if plates else "NOT_FOUND"
    return JSONResponse(content={"plate": plate_number})
