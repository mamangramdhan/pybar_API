from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from PIL import Image
from pyzbar.pyzbar import decode
import httpx
from io import BytesIO

app = FastAPI(
    title="Barcode Reader API",
    description="Scan barcodes and QR codes from image URLs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    image_url: HttpUrl


class BarcodeResult(BaseModel):
    type: str
    data: str


@app.get("/")
def home():
    return {"message": "Barcode Reader API is running"}


@app.post("/scan", response_model=list[BarcodeResult])
async def scan(payload: ScanRequest):
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(str(payload.image_url))
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch image: {e}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"Request error: {e}")

    try:
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid image: {e}")

    decoded_objects = decode(img)

    if not decoded_objects:
        raise HTTPException(status_code=404, detail="No barcode or QR code detected")

    return [
        BarcodeResult(type=obj.type, data=obj.data.decode("utf-8"))
        for obj in decoded_objects
    ]
