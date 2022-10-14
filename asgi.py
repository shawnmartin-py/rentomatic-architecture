from venv import create
from application.fastapi.app import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("asgi:app", reload=True)