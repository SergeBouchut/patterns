from multiprocessing import Process
from threading import Thread
from time import time

from gevent import spawn, wait


COUNT = 100_000_000


def countdown(number):
    start_time = time()
    while number > 0:
        number -= 1
    print(time() - start_time)


# Single process / single thread: ~8s
countdown(COUNT)

# Single process / two threads: ~16+s
t1 = Thread(target=countdown, args=(COUNT // 2,))
t2 = Thread(target=countdown, args=(COUNT // 2,))
t1.start()
t2.start()
t1.join()
t2.join()

# Two processes: ~8+s
p1 = Process(target=countdown, args=(COUNT // 2,))
p2 = Process(target=countdown, args=(COUNT // 2,))
p1.start()
p2.start()
p1.join()
p2.join()

# Using gevent: ~8-s
jobs = [spawn(countdown, COUNT // 2) for _ in range(2)]
wait(jobs)
