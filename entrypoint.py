#!/root/PycharmProjects/GoogleChromeTranslateDictionary/venv/bin/python3
import os

import config
from config import logger
from services import keyboard_handler


@logger.catch()
def main():
    print(os.getpid())
    keyboard_handler.join_listener()


if __name__ == '__main__':
    main()

