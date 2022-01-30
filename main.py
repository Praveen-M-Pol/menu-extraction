import os
import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from core import run_on_single_image
from loguru import logger
from PIL import Image
from io import BytesIO

class Request(BaseModel):
    base64: str

app = FastAPI(title = "Extracting Menu", 
              description="API for extracting text from menu image",
              version='1.0.0')

@app.post("/base64")
def menu_extraction_base64(payload: Request):
    logger.info("Received payload from the base64 endpoint")
    img_base64 = payload.base64
    logger.info("Converting Base64 to PIL image")
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    menu = run_on_single_image(img)
    logger.debug("Sending Response = {}".format(menu))
    return menu

@app.post("/imageupload")
def menu_extraction_upload_image(image: UploadFile = File(...)):
    logger.info("Received image file from the image upload endpoint")
    img = Image.open(image.file)
    menu = run_on_single_image(img)
    logger.success("Sending Response = {}".format(menu))
    return menu
