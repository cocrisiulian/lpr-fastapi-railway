from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import numpy as np
import easyocr

app = FastAPI()
reader = easyocr.Reader(['en', 'ro'], gpu=False)

@app.post("/predict")
async def predict(request: Request):
    try:
        image_bytes = await request.body()
        print("Received bytes:", len(image_bytes))
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        np_img = np.array(image)
        results = reader.readtext(np_img)
        plates = [text for _, text, _ in results]
        plate_number = max(plates, key=len) if plates else "NOT_FOUND"
        return JSONResponse(content={"plate": plate_number})
    except Exception as e:
        print("Exception:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
