import sys


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        try:
            file = open(self.path, "r")
        except Exception as e:
            return(e)

        content = file.read()
        if self.check_structure(content, has_header):
            content_list = []
            for line in content.split("\n")[has_header:]:
                content_list.append(self.to_list(line))
            return content_list
        else:
            return Exception("Invalid file structure")

    def to_list(self, line: str):
        if line == "0,1":
            return [0, 1]
        if line == "1,0":
            return [1, 0]

    def check_structure(self, content: str, has_header: bool):
        lines = content.split("\n")
        if has_header:
            flag = (len(lines) >= 2) and (len(lines[0].split(",")) == 2)
        else:
            flag = len(lines) >= 1

        for line in lines[has_header:]:
            if line not in ["0,1", "1,0"]:
                flag = False
                break
        return flag

    class Calculations:
        def counts(self, list):
            heads = 0
            tails = 0
            for i in list:
                if i == [1, 0]:
                    heads += 1
                else:
                    tails += 1
            return heads, tails

        def fractions(self, heads, tails):
            sum = heads + tails
            return heads/sum * 100, tails/sum*100


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        raise Exception("Invalid number of arguments")
    path = sys.argv[1]
    research = Research(path)

    if len(sys.argv) > 2:
        arr = research.file_reader(sys.argv[2] == "True")
    else:
        arr = research.file_reader()

    print(arr)
    calc = Research.Calculations()
    count = calc.counts(arr)
    print(count[0], count[1])
    frac = calc.fractions(*count)
    print(frac[0], frac[1])



if __name__ == "__main__":
    main()
