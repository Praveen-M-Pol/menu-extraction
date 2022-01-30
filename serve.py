import uvicorn
from main import app
from loguru import logger

logger.add(
    "./logs/menu_extraction.log",
    level='DEBUG',
    backtrace=True,
    diagnose=False,
    rotation="1 day"
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
