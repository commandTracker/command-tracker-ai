from dotenv import load_dotenv
load_dotenv()

from config.rabbitmq import connect
from rabbitmq.consume import consume_message

def main():
    connect()
    consume_message()

if __name__ == "__main__":
    main()
