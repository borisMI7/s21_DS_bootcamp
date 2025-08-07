import timeit


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

    t_loop = timeit.timeit(lambda: loop_and_append(repEmails), number=90000000)
    t_comp = timeit.timeit(lambda: list_comprehension(repEmails), number=90000000)

    if t_comp <= t_loop:
        print("it is better to use a list comprehension")
        print(f"{t_comp} vs {t_loop}")
    else:
        print("it is better to use a loop")
        print(f"{t_loop} vs {t_comp}")

if __name__ == "__main__":
    main()