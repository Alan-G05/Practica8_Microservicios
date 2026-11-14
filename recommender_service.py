import pickle
from fastapi import FastAPI

app = FastAPI(title="Recomendaciones")

with open("../similarity.pkl", "rb") as file:
    datos = pickle.load(file)
sim_g = datos["similares"]

@app.get("/recommends/{song_index}")
def obtener_recomendaciones(song_index: int, top_n: int = 5):
    similares = sorted(
        list(enumerate(sim_g[song_index])),
        reverse = True,
        key = lambda x: x[1]
    )
    indices_recomendados = [idx[0] for idx in similares[1:top_n + 1]]
    return {
        "indices_recomendados": indices_recomendados
    }