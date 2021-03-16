from fastapi import FastAPI
from pydantic import BaseModel
from core import run_on_single_image
from loguru import logger

class Request(BaseModel):
    base64: str

app = FastAPI(title = "Extracting Menu", 
              description="API for extracting text from menu image",
              version='1.0.0')

@app.post("/extractmenu")
def menu_extraction(payload: Request):
    logger.info("Received payload from the endpoint")
    img_base64 = payload['base64']
    menu = run_on_single_image(img_base64)
    logger.info("Sending Response = {}".format(menu))
    return menu
