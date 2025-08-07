import sys


def main():
    if len(sys.argv) > 1:
        do_task(sys.argv[1])


def do_task(task):
    clients = [
        "andrew@gmail.com",
        "jessica@gmail.com",
        "ted@mosby.com",
        "john@snow.is",
        "bill_gates@live.com",
        "mark@facebook.com",
        "elon@paypal.com",
        "jessica@gmail.com",
    ]

    participants = [
        "walter@heisenberg.com",
        "vasily@mail.ru",
        "pinkman@yo.org",
        "jessica@gmail.com",
        "elon@paypal.com",
        "pinkman@yo.org",
        "mr@robot.gov",
        "eleven@yahoo.com",
    ]
    recipients = ["andrew@gmail.com", "jessica@gmail.com", "john@snow.is"]

    if task == "call_center":
        print(call_center(clients, recipients))
    elif task == "potential_clients":
        print(potential_clients(clients, participants))
    elif task == "loyalty_program":
        print(loyalty_program(clients, participants))
    else:
        raise Exception("Unknown command")


def call_center(clients, recipients):
    c_set = set(clients)
    r_set = set(recipients)
    return list(c_set - r_set)


def potential_clients(clients, participants):
    c_set = set(clients)
    p_set = set(participants)
    return list(p_set - c_set)


def loyalty_program(clients, participants):
    c_set = set(clients)
    p_set = set(participants)
    return list(c_set - p_set)


if __name__ == "__main__":
    main()
