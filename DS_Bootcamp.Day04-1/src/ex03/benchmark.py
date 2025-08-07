import timeit
import sys
from functools import reduce


def loop_func(x):
    sum = 0
    for i in range(1, x+1):
        sum = sum + i*i
    return sum

def reduce_func(x):
    return reduce(lambda x, y: x + y*y, range(0, x+1))


def main():
    if len(sys.argv) != 4:
        raise Exception("incorrect number of arguments")

    if sys.argv[1] == "loop":
        t = timeit.timeit(lambda: loop_func(int(sys.argv[3])), number= int(sys.argv[2]))
    elif sys.argv[1] == "reduce":
        t = timeit.timeit(lambda: reduce_func(int(sys.argv[3])), number= int(sys.argv[2]))
    else:
        raise Exception("incorrect method name")

    print(t)

if __name__ == "__main__":
    main()