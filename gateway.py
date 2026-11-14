import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

URL_CATALOG = "http://127.0.0.1:5002"
URL_RECOMMENDER = "http://127.0.0.1:5003"

@app.get("/examples")
async def gateway_examples():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{URL_CATALOG}/examples")
        return resp.json()

@app.post("/recommendations")
async def gateway_recommendations(query: str):
    if not query or query.strip() == "":
        return {"error": "La búsqueda no puede estar vacía."}

    async with httpx.AsyncClient() as client:
        search_resp = await client.get(f"{URL_CATALOG}/search", params={"query": query})
        if search_resp.status_code == 404:
            return {"message": "Esta canción aun no se encuentra en la biblioteca."}

        song_data = search_resp.json()
        song_index = song_data["index"]

        infer_resp = await client.get(f"{URL_RECOMMENDER}/recommends/{song_index}")
        indices = infer_resp.json()["indices_recomendados"]

        details_resp = await client.post(f"{URL_CATALOG}/details", json={"indices": indices})
        return details_resp.json()