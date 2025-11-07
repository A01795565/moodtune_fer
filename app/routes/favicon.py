from base64 import b64decode
from fastapi import FastAPI
from fastapi.responses import Response


def register_favicon(app: FastAPI) -> None:
    # 1x1 transparent PNG served at /favicon.ico
    png_1x1_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    )
    png_bytes = b64decode(png_1x1_base64)

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return Response(content=png_bytes, media_type="image/png")

