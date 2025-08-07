class Research:
    def file_reader():
        try:
            file = open("data.csv", "r")
            return(file.read())
        except Exception as e:
            return(e)


def main():
    print(Research.file_reader())

if __name__ == "__main__":
    main()