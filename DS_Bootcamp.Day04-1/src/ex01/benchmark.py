import timeit


def list_map(emails):
    return list(map(lambda x: x if x.endswith("@gmail.com") else None, emails))

def loop_and_append(emails):
    result = []
    for email in emails:
        if(email.endswith('@gmail.com')):
            result.append(email)
    return result

def list_comprehension(emails):
    return [email for email in emails if email.endswith('@gmail.com')]

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
    'anna@live.com', 'philipp@gmail.com']

    repEmails = []
    for i in range(0, 5):
        repEmails.extend(emails)

    times_dict = {}

    times_dict["loop"] = timeit.timeit(lambda: loop_and_append(repEmails), number=90000000)
    times_dict["list_comprehension"] = timeit.timeit(lambda: list_comprehension(repEmails), number=90000000)
    times_dict["map"] = timeit.timeit(lambda: list_map(repEmails), number=90000000)

    order = sorted(times_dict, key = lambda x: times_dict[x])
    phrase_dict = {"map":"it is better to use a map",
                   "list_comprehension": "it is better to use a list comprehension",
                   "loop":"it is better to use a loop"
                  }
    print(phrase_dict[order[0]])
    print(f"{times_dict[order[0]]} vs {times_dict[order[1]]} vs {times_dict[order[2]]}")

if __name__ == "__main__":
    main()