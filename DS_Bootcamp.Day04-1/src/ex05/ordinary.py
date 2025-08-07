import sys
import resource
import time

def list_creator(path):
    with open(path) as file:
        lines = file.read().split("\n")
    return lines


def main():

    start_time = time.time()
    if len(sys.argv) != 2:
        raise Exception("incorrect number of arguments")
    list = list_creator(sys.argv[1])

    for i in list:
        pass
    end_time = time.time()

    total_time = end_time - start_time
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_memory_gb = peak_memory / (1024 ** 3)

    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

if __name__ == "__main__":
    main()