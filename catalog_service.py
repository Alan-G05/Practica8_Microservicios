import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="catalogo")

with open("../similarity.pkl", "rb") as file:
    df = pickle.load(file)
df_g = df["df"][["song", "artist"]]

class SongRequest(BaseModel):
    indices: list[int]

@app.get("/examples")
def obtenerEjemplos(cantidad: int = 5):
    ejemplos = df_g.sample(cantidad)
    return [
        {"title": song, "artist": artist}
        for song, artist in zip(ejemplos["song"], ejemplos["artist"])
    ]

@app.get("/search")
def buscar_cancion(query: str):
    cancion = df_g[df_g["song"].str.lower() == query.lower().strip()]
    if cancion.empty:
        raise HTTPException(status_code=404, detail="Canción no encontrada")

    indice = cancion.index[0]
    return {
        "index": indice,
        "title": df_g.loc[indice, "song"],
        "artist": df_g.loc[indice, "artist"]
    }

@app.post("/details")
def obtener_detalles(req: SongRequest):
    resultados = []
    for idx in req.indices:
        resultados.append({
            "title": df_g.iloc[idx]["song"],
            "artist": df_g.iloc[idx]["artist"]
        })
    return resultados