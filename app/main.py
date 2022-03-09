from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Root"])
def read_root()-> dict:
    return {"message": "welcome to FastAPI!"}