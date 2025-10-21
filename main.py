from fastapi import FastAPI

from app.router import router

app = FastAPI(title='String Analyzer')
app.include_router(router)

@app.get('/')
def read_root():
    return {"message": "Welcome!"}
