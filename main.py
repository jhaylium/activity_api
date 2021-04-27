from fastapi import FastAPI
from typing import Optional
from app.routes import activity, infrastructure, marketing
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ['http://localhost:8000', 'metadata.surveydatahub.com',
           'dev-app.surveydatahub.com', 'http://localhost', 'app.surveydatahub.com',
           'surveydatahub.com', '*.surveydatahub.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(activity.router, prefix="/activity")
app.include_router(marketing.router, prefix="/marketing")
app.include_router(infrastructure.router, prefix="/infra")



@app.get("/")
def read_root():
    return {"status": "Welcome to the SDH Activity API"}







