def main():
    list_of_tuples = [
        ("Russia", "25"),
        ("France", "132"),
        ("Germany", "132"),
        ("Spain", "178"),
        ("Italy", "162"),
        ("Portugal", "17"),
        ("Finland", "3"),
        ("Hungary", "2"),
        ("The Netherlands", "28"),
        ("The USA", "610"),
        ("The United Kingdom", "95"),
        ("China", "83"),
        ("Iran", "76"),
        ("Turkey", "65"),
        ("Belgium", "34"),
        ("Canada", "28"),
        ("Switzerland", "26"),
        ("Brazil", "25"),
        ("Austria", "14"),
        ("Israel", "12"),
    ]

    new_dict = {}
    for value, key in list_of_tuples:
        if not key in new_dict.keys():
            new_dict[key] = []
        new_dict[key].append(value)

    print_dict(new_dict)


def print_dict(d: dict):
    for key in d:
        for value in d[key]:
            print("'" + key, value + "'", sep="' : '")


if __name__ == "__main__":
    main()
