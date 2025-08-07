class Must_read:
    try:
        file = open("data.csv", "r")
        print(file.read())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    Must_read()