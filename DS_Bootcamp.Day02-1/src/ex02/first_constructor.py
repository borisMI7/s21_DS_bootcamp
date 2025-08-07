import sys

class Research:

    def __init__(self, path):
        self.path = path

    def file_reader(self):
        try:
            file = open(self.path, "r")
        except Exception as e:
            return(e)

        content = file.read()
        if self.check_structure(content):
            return content
        else:
            return Exception("Invalid file structure")

    def check_structure(self, content):
        lines = content.split("\n")
        flag = (len(lines) >= 2) and (len(lines[0].split(",")) == 2)
        for line in lines[1:]:
            if line not in ["0,1", "1,0"]:
                flag = False
                break
        return flag


def main():
    if len(sys.argv) != 2:
        raise Exception("Invalid number of arguments")
    path = sys.argv[1]
    research = Research(path)
    print(research.file_reader())

if __name__ == "__main__":
    main()