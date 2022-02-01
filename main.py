import os
import base64
from PIL import Image
from io import BytesIO
from loguru import logger
from fastapi import FastAPI, File, UploadFile


from core import run_for_simple_menu, run_for_description_menu
from models import Request


tags_metadata = [
    {
        "name": "Simple Menu",
        "description": "Endpoints for menu with only name and price"
    },
    {
        "name": "Description Menu",
        "description": "Endpoints for menu with name, price and description"
    }
]



app = FastAPI(
    title = "Extracting Menu", 
    description="API for extracting dish name and price from image of menu",
    openapi_tags=tags_metadata,
    version='1.0.0'
)


@app.post("/simplemenu/base64", tags=["Simple Menu"])
def simple_menu_extraction_base64(payload: Request):
    logger.info("Received payload from the base64 endpoint")
    img_base64 = payload.base64
    logger.info("Converting Base64 to PIL image")
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    menu = run_for_simple_menu(img)
    logger.debug("Sending Response = {}".format(menu))
    return menu


@app.post("/simplemenu/imageupload", tags=["Simple Menu"])
def simple_menu_extraction_upload_image(image: UploadFile = File(...)):
    logger.info("Received image file from the image upload endpoint")
    img = Image.open(image.file)
    menu = run_for_simple_menu(img)
    logger.success("Sending Response = {}".format(menu))
    return menu


@app.post("/descriptionmenu/base64", tags=["Description Menu"])
def description_menu_extraction_base64(payload: Request):
    logger.info("Received payload from the base64 endpoint")
    img_base64 = payload.base64
    logger.info("Converting Base64 to PIL image")
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    menu = run_for_description_menu(img)
    logger.debug("Sending Response = {}".format(menu))
    return menu


@app.post("/descriptionmenu/imageupload", tags=["Description Menu"])
def description_menu_extraction_upload_image(image: UploadFile = File(...)):
    logger.info("Received image file from the image upload endpoint")
    img = Image.open(image.file)
    menu = run_for_description_menu(img)
    logger.success("Sending Response = {}".format(menu))
    return menu
