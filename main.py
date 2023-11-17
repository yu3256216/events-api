from fastapi import FastAPI

from src.application.routers.events_routes import router

app = FastAPI(debug=True)


app.include_router(router)
