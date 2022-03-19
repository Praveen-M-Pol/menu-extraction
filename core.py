import re
from tr import run
from loguru import logger
from fastapi import HTTPException


def load_img_and_run_ocr(img_pil):
    """
        Function for loading, resizing and then running the
        ocr on the image.
    """
    logger.info("Resizing the image")
    MAX_SIZE = 2000
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)
    gray_pil = img_pil.convert("L")

    logger.info("Running OCR on the iamge")
    results = run(gray_pil)
    logger.info("Output of OCR = {}".format(results))
    return results


def filter_text(extract_info_non_fil):
    """
        Function to filter the text where the probability is
        greater than 0.8
    """
    logger.info("Filtering the words from OCR output")
    extract_info = []
    for line in extract_info_non_fil:
        if line[-1] >= 0.8:
            extract_info.append(line)
    
    logger.info("Before filtering, number of words = {}".format(len(extract_info_non_fil)))
    logger.info("After filtering, number of words = {}".format(len(extract_info)))

    return extract_info


def convert_to_required_format(menu):
    """
        Function for converting to required format.
    """
    logger.info("Converting it to required format")
    formatted_menu = {'menus': []}
    for category in menu:
        for item in menu[category]:
            formatted_menu['menus'].append(item)

    return formatted_menu


def extract_simple_menu(extract_info_non_fil):
    """
        function which contains the core logic
        to extract information from ocr output
        for simple menu that is name and price.
    """
    # filtering text from ocr
    extract_info = []
    for line in extract_info_non_fil:
        if (len(line[1]) > 0) and (bool(re.search("[A-Za-z]", line[1][0])) or bool(re.search("[0-9]", line[1][0]))):
            extract_info.append(line)

    # text from ocr
    text = [line[1] for line in extract_info]
    logger.info("Running the core logic on filtered words = {}".format(text))

    # category: {dishname: price} in dict form
    menu = {}
    category_idx = -1
    idx = 0
    while(idx < len(text) - 1):
        # so current starts with character
        if re.search("[A-Za-z]", text[idx][0]):
            # now check if next one also starts with character
            if re.search("[A-Za-z]", text[idx+1][0]):
                category_idx = idx
                # init with empty list
                menu[text[category_idx]] = []
                idx = idx + 1
            # now check if next one starts with number
            elif re.search("[0-9]", text[idx+1][0]):
                item = {
                    "name": text[idx],
                    "price": text[idx + 1]
                }
                menu[text[category_idx]].append(item)
                idx = idx + 2
            else:
                idx = idx + 1
        else:
            idx = idx + 1

    logger.info("Extraction from image = {}".format(menu))
    return menu


def extract_description_menu(extract_info_non_fil):
    """
        function which contains the core logic
        to extract information from ocr output
        for description menu that is name, price and
        description.
    """
    # filtering text from ocr
    extract_info = []
    for line in extract_info_non_fil:
        if (len(line[1]) > 0) and (bool(re.search("[A-Za-z]", line[1][0])) or bool(re.search("[0-9]", line[1][0]))):
            extract_info.append(line)

    # text from ocr
    text = [line[1] for line in extract_info]
    logger.info("Running the core logic on filtered words = {}".format(text))

    # category: {dishname: price} in dict form
    menu = {}
    category_idx = -1
    idx = 0
    while(idx < len(text) - 2):
        # so current starts with character
        if re.search("[A-Za-z]", text[idx][0]):
            # now check if next one also starts with character
            if re.search("[A-Za-z]", text[idx+1][0]):
                category_idx = idx
                # init with empty list
                menu[text[category_idx]] = []
                idx = idx + 1
            # now check if next one starts with number
            elif re.search("[0-9]", text[idx+1][0]):
                item = {
                    "name": text[idx],
                    "price": text[idx + 1],
                    "description": text[idx + 2]
                }
                menu[text[category_idx]].append(item)
                idx = idx + 3
            else:
                idx = idx + 1

    return menu


def run_for_simple_menu(img, dishes):
    try:
        extract_info = load_img_and_run_ocr(img)
        extract_info = filter_text(extract_info)
        menu = extract_simple_menu(extract_info)
        menu = convert_to_required_format(menu)
        menu = put_items_into_categories(menu, dishes)
    except Exception as ex:
        logger.exception("Exception in simple menu = {}".format(str(ex)))
        raise HTTPException(500, detail=str(ex))

    return menu


def run_for_description_menu(img, dishes):
    try:
        extract_info = load_img_and_run_ocr(img)
        extract_info = filter_text(extract_info)
        menu = extract_description_menu(extract_info)
        menu = convert_to_required_format(menu)
        menu = put_items_into_categories(menu, dishes)
    except Exception as ex:
        logger.exception("Exception in description menu= {}".format(str(ex)))
        raise HTTPException(500, detail=str(ex))

    return menu


def put_items_into_categories(menu, dishes):
    # takes input from output of convert_to_required_format
    # categories
    for item in menu["menus"]:
        dish = dishes.loc[dishes["name"] == item["name"].lower()]
        # update item, it will be done in menu I guess
        if len(dish) == 0:
            item["category"] = "other"
        else:
            item["category"] = dish["course"].tolist()[0]

    return menu
