import timeit
import sys


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

def list_filter(emails):
    return list(filter(lambda x: x.endswith("@gmail.com"), emails))

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
    'anna@live.com', 'philipp@gmail.com']

    repEmails = []
    for i in range(0, 5):
        repEmails.extend(emails)

    if sys.argv[1] == "loop":
        t = timeit.timeit(lambda: loop_and_append(repEmails), number = int(sys.argv[2]))
    elif sys.argv[1] == "list_comprehension":
        t = timeit.timeit(lambda: list_comprehension(repEmails), number = int(sys.argv[2]))
    elif sys.argv[1] == "map":
        t = timeit.timeit(lambda: list_map(repEmails), number = int(sys.argv[2]))
    elif sys.argv[1] == "filter":
        t = timeit.timeit(lambda: list_filter(repEmails), number = int(sys.argv[2]))
    else:
        raise Exception("incorrect method name")

    print(t)


if __name__ == "__main__":
    main()