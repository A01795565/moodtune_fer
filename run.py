import os
import uvicorn
from app import create_app


def main() -> None:
    host = os.environ.get("FER_HOST", "0.0.0.0")
    port = int(os.environ.get("FER_PORT", "8081"))
    app = create_app()
    uvicorn.run(app, host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
