from dotenv import load_dotenv
load_dotenv(override=True)

from multiprocessing import Process

from rabbitmq.consume import consume_message
from config.rabbitmq import create_connection

def worker():
    connection, channel = create_connection()

    channel.basic_qos(prefetch_count=1)
    consume_message(channel)
    connection.close()

def main():
    workers = []

    for _ in range(3):
        p = Process(target=worker)

        p.start()
        workers.append(p)

    for p in workers:
        p.join()

if __name__ == "__main__":
    main()
