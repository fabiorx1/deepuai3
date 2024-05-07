from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from models import DeepUaiDataset

app = FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
async def root(): return RedirectResponse('/docs')

@app.get("/ds/{name}/filepaths")
async def dataset_filepaths(name: str):
    ds = DeepUaiDataset(name=name)
    return ds.filepaths