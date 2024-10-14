import os
import time

def wait_for_file(path, filename, retry=20):
    i=1
    res = False
    if not os.path.exists(path):
        raise "Error : path does not exist"
    while not os.path.isfile(os.path.join(path, filename)) and i <= retry:
        time.sleep(1)
        i += 1
    if i <= retry:
        res = True
    return res
