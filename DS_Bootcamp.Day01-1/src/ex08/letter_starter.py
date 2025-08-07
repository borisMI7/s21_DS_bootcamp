import sys


def main():
    if len(sys.argv) == 2:
        email = sys.argv[1]
        names_list = open("employees.tsv", "r").read().split("\n")[1:]
        email_to_name_dict = {
            line.split("\t")[2]: line.split("\t")[0] for line in names_list
        }
        if email in email_to_name_dict.keys():
            name = email_to_name_dict[email]
            print(
                f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."
            )


if __name__ == "__main__":
    main()
