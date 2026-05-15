---
title: Barcode Reader API
emoji: 📷
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Barcode Reader API

FastAPI app to scan barcodes and QR codes from image URLs.

## Endpoint

### `POST /scan`
```json
{
  "image_url": "https://example.com/barcode.jpg"
}
```

### Response
```json
[
  {
    "type": "QR Code",
    "data": "https://example.com"
  }
]
```

## Docs
Visit `/docs` for Swagger UI.
