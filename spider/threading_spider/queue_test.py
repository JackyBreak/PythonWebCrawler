from queue import Queue

if __name__ == "__main__":
    message_queue = Queue(maxsize=2)

    message_queue.put("jacky")

    message_queue.put("jacky1")

    message_queue.put("jacky2")