from time import sleep, time


DURATION = 1


# SYNCHRONOUS
def s_stack(stack, item):
    sleep(DURATION)
    stack.add((item, int(time() - start)))

start = time()
stacked = set()
to_stack = ['hello', 'world']

while to_stack:
    item = to_stack.pop(0)
    s_stack(stacked, item)
assert stacked == {('hello', 1), ('world', 2)}


# ASYNCHRONOUS
def coroutine(func):
    def starter(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return starter

@coroutine
def a_sleep(count):
    start_sleep = time()
    while (time() - start_sleep) < count:
        yield True

@coroutine
def a_stack(stack, item):
    while True:
        yield
        yield from a_sleep(DURATION)
        stack.add((item, int(time() - start)))

start = time()
stacked = set()
to_stack = [a_stack(stacked, 'hello'), a_stack(stacked, 'world')]

while to_stack:
    item = to_stack.pop(0)
    if item.send(None):
        to_stack.append(item)
assert stacked == {('hello', 1), ('world', 1)}
