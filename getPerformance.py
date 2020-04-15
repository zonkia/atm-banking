import time


def get_performance(func, iterations=1, *arg):
    start = time.perf_counter()
    for i in range(0, iterations):
        func(*arg)
        i
    end = time.perf_counter()
    return end - start
