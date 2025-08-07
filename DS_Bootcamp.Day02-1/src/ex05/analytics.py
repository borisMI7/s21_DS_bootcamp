from random import randint

class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        try:
            file = open(self.path, "r")
        except Exception as e:
            raise e

        content = file.read()
        if self.check_structure(content, has_header):
            content_list = []
            for line in content.split("\n")[has_header:]:
                content_list.append(self.to_list(line))
            return content_list
        else:
            raise Exception("Invalid file structure")

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
        def __init__(self, list):
            self.list = list

        def counts(self):
            heads = 0
            tails = 0
            for i in self.list:
                if i == [1, 0]:
                    heads += 1
                else:
                    tails += 1
            return tails, heads

        def fractions(self, heads, tails):
            sum = heads + tails
            return heads/sum * 100, tails/sum*100

    class Analytics(Calculations):

        def save_data(self, data, name_of_file, extension):
            file = open(name_of_file + '.' + extension, 'w')
            file.write(data)


        def predict_random(self, number):
            list = []
            for i in range(0, number):
                rnd = randint(0, 1)
                sublist = [rnd, int(rnd == 0)]
                list.append(sublist)
            return list

        def predict_last(self, arr):
            return arr[-1]