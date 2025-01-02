import numpy as np
import time


def stats_decorator(func):
    exec_times = []

    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        exec_times.append(end - start)

        if len(exec_times) == 0:
            print("funkcja nie była jeszcze wykonywana")
        else:
            print("funckja była wykonywana ", len(exec_times), "razy")
            print("czas wykonania funkcji: ", exec_times[-1], "sekund")
            print("średni czas wykonania funkcji: ", np.round(np.mean(exec_times), 5), "sekund")
            print("minimalny czas wykonania funkcji: ", np.round(np.min(exec_times), 5), "sekund")
            print("maksymalny czas wykonania funkcji: ", np.round(np.max(exec_times), 5), "sekund")
            print("odchylenie standardowe czasu wykonania funkcji: ", np.round(np.std(exec_times), 5), "sekund")
            print("#######################################################")
    return wrapper


@stats_decorator
def function(n):
    X = np.random.rand(n, n)
    Y = np.random.rand(n, n)
    Z = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Z[i, j] = np.sqrt(X[i, j] ** 2 + Y[i, j] ** 2)
    return Z


function(1000)
function(1000)
function(1000)
