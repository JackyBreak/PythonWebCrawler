from threading import Thread
from threading import Lock

total = 0
total_lock = Lock()

def add():
    total_lock.acquire()
    global total
    for i in range(1000000):
        total += 1
    total_lock.release()

def desc():
    total_lock.acquire()
    global total
    for i in range(1000000):
        total -= 1
    total_lock.release()

if __name__ == "__main__":
    add_thread = Thread(target=add)
    desc_thread = Thread(target=desc)

    add_thread.start()
    desc_thread.start()

    add_thread.join()
    desc_thread.join()
    print(total)