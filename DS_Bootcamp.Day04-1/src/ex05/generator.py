import sys
import resource
import time

def generator_creator(path):
    with open(path) as file:
        for line in file:
            yield line


def main():

    start_time = time.time()
    if len(sys.argv) != 2:
        raise Exception("incorrect number of arguments")
    generator = generator_creator(sys.argv[1])

    for i in generator:
        pass
    end_time = time.time()

    total_time = end_time - start_time
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_memory_gb = peak_memory / (1024 ** 3)

    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

if __name__ == "__main__":
    main()