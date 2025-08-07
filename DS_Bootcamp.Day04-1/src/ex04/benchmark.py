import timeit
import random
from collections import Counter



def with_to_dict(list):
    return Counter(list)

def with_top_10(list):
    dict = with_to_dict(list)
    return [x[0] for x in dict.most_common(10)]

def without_to_dict(list):
    dict = {}
    for i in list:
        if i in dict.keys():
            dict[i] += 1
        else:
            dict[i] = 1
    return dict

def without_top_10(list):
   dict = without_to_dict(list)
   return sorted(dict, key = lambda x: dict[x], reverse= True)[:10]

def main():
    list = [random.randint(0, 100) for i in range(0, 1000000)]

    myF_t = timeit.timeit(lambda: without_to_dict(list), number = 1)
    CF_t = timeit.timeit(lambda: with_to_dict(list), number = 1)
    myT_t = timeit.timeit(lambda: without_top_10(list), number = 1)
    CT_t = timeit.timeit(lambda: with_top_10(list), number = 1)

    print("my function:", myF_t)
    print("Counter:", CF_t)
    print("my top:", myT_t)
    print("Counter's top:", CT_t)

if __name__ == "__main__":
    main()

