import sys


def main():
    if len(sys.argv) == 2:
        emails = open(sys.argv[1], "r").read().split("\n")
        new_file = open("employees.tsv", "w")
        new_file.write("Name\tSurname\tE-mail\n")
        for e in emails[:-1]:
            name, surname = get_name(e)
            new_file.write(name + "\t" + surname + "\t" + e + "\n")
        e = emails[-1]
        name, surname = get_name(e)
        new_file.write(name + "\t" + surname + "\t" + e)


def get_name(email: str):
    name = email.split(".")[0].capitalize()
    surname = email.split(".")[1].split("@")[0].capitalize()
    return name, surname


if __name__ == "__main__":
    main()
