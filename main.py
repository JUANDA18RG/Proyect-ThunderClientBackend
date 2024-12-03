from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from db import check_connection
from routes.products import router as product_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product_router, tags=["products"])


@app.get('/', tags=['home'])
async def message():
    connection_status = await check_connection()
    return HTMLResponse(f'<h1>{connection_status}</h1>')


# source venv/bin/activate
# uvicorn main:app --reload --port 8001
