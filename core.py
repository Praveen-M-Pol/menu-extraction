import re
import base64
from loguru import logger
from io import BytesIO
from PIL import Image
from tr import run

def load_img_and_run_ocr(img_pil):
    MAX_SIZE = 2000
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)

    gray_pil = img_pil.convert("L")
    results = run(gray_pil)
    return results

def extract_menu(extract_info_non_fil):
    # filtering text from ocr
    extract_info = []
    for line in extract_info_non_fil:
        if bool(re.search("[A-Za-z]", line[1][0])) or bool(re.search("[0-9]", line[1][0])):
            extract_info.append(line)

    # category:{dishname : price} in dict form
    menu = {}
    category_idx = -1
    idx = 0
    while(idx < len(extract_info)):
        # so current starts with character
        if re.search("[A-Za-z]", extract_info[idx][1][0]):
            # now check if next one also starts with character
            if re.search("[A-Za-z]", extract_info[idx+1][1][0]):
                category_idx = idx
                # init with empty dict
                menu[extract_info[category_idx][1]] = {}
                idx = idx + 1
            # now check if next one starts with number
            elif re.search("[0-9]", extract_info[idx+1][1][0]):
                menu[extract_info[category_idx][1]][extract_info[idx][1]] = extract_info[idx+1][1]
                idx = idx + 2
            else:
                idx = idx + 1
        else:
            idx = idx + 1

    return menu

def convert_to_required_format(menu):
    formatted_menu = {'menus':[]}
    for category in menu:
        formatted_menu['category'] = category
        for name, price in menu[category].items():
            formatted_menu['menus'].append({'name':name, 'price':price})
    
    return formatted_menu

def run_on_single_image(img_base64):
    logger.info("Converting Base64 to PIL image")
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    logger.info("Running OCR on the iamge")
    extract_info = load_img_and_run_ocr(img)
    logger.info("Running extraction logic on OCR results")
    menu = extract_menu(extract_info)
    logger.info("Converting it to required format")
    menu = convert_to_required_format(menu)
    return menu
