from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import incidentsRoute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + Redis project by the team 5! "}


app.include_router(incidentsRoute.router, tags=["Incidents"], prefix="/api/v1")
