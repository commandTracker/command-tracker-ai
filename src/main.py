from dotenv import load_dotenv
load_dotenv()

import os

from config.rabbitmq import connect
from rabbitmq.consume import consume_message

def main():
    if not os.path.exists("temp"):
        os.makedirs("temp")

    connect()
    consume_message()

if __name__ == "__main__":
    main()
