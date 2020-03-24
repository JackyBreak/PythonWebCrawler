import time
from threading import Thread

def sleep_task(sleeptime):
    print("sleep {} second start!".format(sleeptime))
    time.sleep(sleeptime)
    print("sleep {} second end!".format(sleeptime))

class SleepThread(Thread):
    def __init__(self, sleeptime):
        self.sleeptime = sleeptime
        super().__init__()

    def run(self):
        print("sleep {} second start!".format(self.sleeptime))
        time.sleep(self.sleeptime)
        print("sleep {} second end!".format(self.sleeptime))


if __name__ == "__main__":
    start_time = time.time()
    t1 = Thread(target=sleep_task, args=(2,))
    t1.setDaemon(True)
    t1.start()

    t2 = Thread(target=sleep_task, args=(3,))
    t2.setDaemon(True)
    t2.start()
    #
    # t1.join()
    # t2.join()
    time.sleep(1)
    end_time = time.time()
    print("last time: {}".format(end_time - start_time))

if __name__ == "__main__":
    t1 = SleepThread(2)
    t2 = SleepThread(3)
    t1.start(2)
    t2.start(3)