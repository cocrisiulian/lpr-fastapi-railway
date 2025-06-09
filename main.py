from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import pytesseract

app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    image_bytes = await request.body()  # primește imaginea direct din body
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    plate_number = pytesseract.image_to_string(image, config='--psm 7')
    plate_number = ''.join(filter(str.isalnum, plate_number))
    return JSONResponse(content={"plate": plate_number})
