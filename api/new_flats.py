from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
async def get_new_flats():
    with open('api_new_flats.json', 'r', encoding='utf-8') as f:
        new_flats = json.loads(f.read())
    return {"message": new_flats}