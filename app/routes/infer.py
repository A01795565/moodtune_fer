from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from ..src.predictor import FerPredictor


def register_infer(app: FastAPI, predictor: FerPredictor) -> None:
    @app.post("/infer")
    async def infer(image: UploadFile = File(...)):
        if image.content_type not in ("image/png", "image/jpeg", "image/jpg"):
            raise HTTPException(status_code=400, detail="Formato no soportado. Usa PNG o JPG.")
        data = await image.read()
        out = predictor.predict(data)
        return JSONResponse(out)

    # Provide a friendly GET handler to avoid 405s when
    # users or health checks hit `/infer` in a browser.
    @app.get("/infer", include_in_schema=False)
    async def infer_info():
        return JSONResponse(
            {
                "endpoint": "/infer",
                "method": "POST",
                "field": "image",
                "content_types": ["image/png", "image/jpeg", "image/jpg"],
                "message": "Envía una imagen usando POST multipart/form-data en el campo 'image'.",
            }
        )
