from fastapi import FastAPI, Request
from app.router import router


app = FastAPI(title='String Analyzer')
app.include_router(router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    print('\n\n')
    print(f"➡️  {request.method} {request.url}")
    try:
        body = await request.json()
        print(f"📦 Body: {body}")
    except Exception:
        print("📭 No JSON body")

    print('\n\n')


    response = await call_next(request)
    return response


@app.get('/')
def read_root():
    return {"message": "Welcome!"}
