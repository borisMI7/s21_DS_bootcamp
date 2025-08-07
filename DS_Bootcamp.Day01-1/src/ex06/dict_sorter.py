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

    d = dict(list_of_tuples)

    new_dict = {}
    for value, key in list_of_tuples:
        key = int(key)
        if not key in new_dict.keys():
            new_dict[key] = []
        new_dict[key].append(value)

    for key in sorted(new_dict.keys(), reverse=True):
        new_dict[key].sort()
        for word in new_dict[key]:
            print(word)


if __name__ == "__main__":
    main()
