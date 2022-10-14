from fastapi import FastAPI

from application.fastapi.rest import room

def create_app():
    app = FastAPI()

    app.include_router(room.router)

    return app