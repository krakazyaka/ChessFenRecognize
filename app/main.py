import uuid
import shutil
from fastapi import FastAPI, File, UploadFile

from .predictor import display_with_predicted_fen

app = FastAPI()

# Методы API


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)) -> str:
    myuuid = uuid.uuid4()
    with open("/code/app/media/" + str(myuuid) + ".jpeg", "wb") as image:
        shutil.copyfileobj(file.file, image)
    return {"Id": myuuid}

@app.get("/fen")
async def get_fen(code):
    fen = display_with_predicted_fen(code)
    return fen
