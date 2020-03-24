from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import time

def sleep_task(sleeptime):
    time.sleep(sleeptime)
    print("sleep {}s".format(sleeptime))
executor = ThreadPoolExecutor(max_workers=2)
task1 = executor.submit(sleep_task, 2)
time.sleep(3)
print(task1.done())