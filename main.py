import uuid
import shutil
import keras.models
from fastapi import FastAPI, File, UploadFile

import predictor

app = FastAPI()
model = keras.models.load_model("chess_model.h5")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)) -> str:
    myuuid = uuid.uuid4()
    with open("media/" + str(myuuid) + ".jpeg", "wb") as image:
        shutil.copyfileobj(file.file, image)
    return {"Id": myuuid}

@app.get("/fen")
async def get_fen(code):
    fen = predictor.display_with_predicted_fen(code)
    return fen
