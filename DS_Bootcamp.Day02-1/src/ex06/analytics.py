from random import randint
import logging
import urllib.request
import urllib.parse


class Research:
    def __init__(self, path):
        self.path = path

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("analytics.log")
        formatter = logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("Research class init")

    def telegram_message(self, status_ok:bool):
        if status_ok:
            msg = urllib.parse.quote_plus("The report has been successfully created")
        else:
            msg = urllib.parse.quote_plus("The report hasn't been created due to an error")
        urllib.request.urlopen('https://api.telegram.org/bot8106730857:AAHeIPVziZrHd3L1wske-BQcOrr7KpST6DY/sendMessage?chat_id=@s21_day02&text=' + msg)


    def file_reader(self, has_header=True):
        self.logger.info("Reading the file " + self.path + ", has header = " + str(has_header))
        try:
            file = open(self.path, "r")
        except Exception as e:
            raise e

        content = file.read()
        if self.check_structure(content, has_header):
            content_list = []
            for line in content.split("\n")[has_header:]:
                sublist = [int(x) for x in line.split(',')]
                content_list.append(sublist)
            return content_list
        else:
            raise Exception("Invalid file structure")

    def check_structure(self, content: str, has_header: bool):
        self.logger.info("Checking file structure")
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

            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)

            self.logger.info("Calculations class init")

        def counts(self):
            self.logger.info("Calculating the counts of heads and tails")
            heads = self.list.count([1, 0])
            tails = self.list.count([0, 1])
            return tails, heads

        def fractions(self, heads, tails):
            self.logger.info("Calcilating fractions, heads = " + str(heads) + ", tails = " + str(tails))
            sum = heads + tails
            return heads/sum * 100, tails/sum*100

    class Analytics(Calculations):

        def save_data(self, data, name_of_file, extension):
            self.logger.info("Saving data to " + name_of_file + "." + extension)
            file = open(name_of_file + '.' + extension, 'w')
            file.write(data)


        def predict_random(self, number):
            self.logger.info("Predicting " + str(number) + " random results")
            list = []
            for i in range(0, number):
                rnd = randint(0, 1)
                sublist = [rnd, int(rnd == 0)]
                list.append(sublist)
            return list

        def predict_last(self, arr):
            self.logger.info("Predicting last result")
            return arr[-1]