import os, sys, urllib, requests, bs4, json,\
pytest, collections, functools, datetime, re


class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file, path_to_movies='../datasets/ml-latest-small/movies.csv', dump_file_path = 'big_list.json'):
        """
        Put here any fields that you think you will need.
        """
        self.file = path_to_the_file
        self.moves_file = path_to_movies
        self.dump_file = dump_file_path

    def __dump_all_data__(self, dump_file_path, max_lines = 10000):
        big_list = list()
        fields = ['Director', 'Budget', 'Gross worldwide', 'Runtime']

        with open(self.file) as file:
            #get rid of title
            line_cnt = 1
            file.readline()

            for line in file:
                imdb_id = line.split(',')[1]
                try:
                    #big_list.append(self.__useful_dict__(imdb_id))
                    print('trying to get IMDb_id ', imdb_id)
                    big_list.append(self.get_imdb([imdb_id], fields)[0])
                except Exception as e:
                    with open("errors.txt", 'a+') as err_file:
                        print(f'Error {e.args} ocurred ', f'not upload move №{line_cnt} with IMDb_id {imdb_id}', file=err_file)

                if line_cnt > max_lines:
                    break

                print(f'upload move №{line_cnt} with IMDb_id {imdb_id}')
                line_cnt += 1

        with open(dump_file_path, 'w+') as dump_file:
            print(json.dumps(big_list), file=dump_file)


    @staticmethod
    def __useful_dict__(move_id: str):
        '[movieId, Director, Budget, Cumulative Worldwide Gross, Runtime]'
        useful_data = dict()

        url = f'https://www.imdb.com/title/tt{move_id}/'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        #найдем все теги с списками на странице и пробежимс по ним
        j_data = soup.find_all('li', class_=re.compile(r'ipc-metadata-list__item ipc-metadata-list__item--align-end'))
        for line in j_data:

            #просматриваем все ссылки в валидных тегах
            val_tags = line.find_all(re.compile(r'(span|a)'))
            #и запихиваем не нулевые в список
            tag_list = [elem.string for elem in val_tags if elem.string is not None]
            #а потом перезапихиваем в словарь
            if len(tag_list) >= 2:
                #денежные значения типа $100,000,000 приведем к инту
                if tag_list[1][0] in '€$£':
                    repl = tag_list[1][1:].replace(',' , '')
                    tag_list[1] = int(re.search(r'\d+', repl).group(0))
                useful_data[tag_list[0]] = tag_list[1:]

            #обрабатываем runtime - он отличается кривым выводом:
            #1<!-- --> <!-- -->hour<!-- --> <!-- -->21<!-- --> <!-- -->minutes
            if len(tag_list) == 1 and 'Runtime' in tag_list[0]:
                runstr = line.find('div')

                subrun = re.search(r'\d+.+\d+', str(runstr))
                if subrun:
                    subrun = subrun.group(0)
                    hours = re.search(r'^\d+', subrun)
                    minutes = re.search(r'\d+$', subrun)
                    if hours and minutes:
                        useful_data[tag_list[0]] = [int(hours.group(0)) * 60 + int(minutes.group(0))]

            #print(tag_list)
            #print(line)
            
        return useful_data
    
    def __convert_money__(self):
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for elem in big_list:
            try:
                int(elem[2][0])
            except ValueError:
                res = elem[2][0].replace(',' , '')
                res = re.search(r'\d+', res)
                if res:
                    elem[2][0] = int(res.group(0))
            except TypeError:
                pass

        with open(self.dump_file, 'w') as dump_file:
            print(json.dumps(big_list), file=dump_file)



    @staticmethod
    def get_imdb(list_of_movies: list, list_of_fields: list) -> list:
        """
The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
     Sort it by movieId descendingly.
        """
        imdb_info = list()
        for move_id in list_of_movies:
            useful_dict = Links.__useful_dict__(str(move_id))
            sublist = [move_id]
            for filed in list_of_fields:
                try:
                    sublist.append(useful_dict[filed])
                except KeyError as e:
                    print(f"No key: {filed} found")
                    sublist.append([None])
            imdb_info.append(sublist)
        
        return imdb_info
            
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        directors = dict()
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for film_data in big_list:
            directors[film_data[1][0]] = directors.get(film_data[1][0], 0) + 1
        directors.pop(None, None)
        directors = {k: v for k ,v in sorted(directors.items(), key=lambda x: x[1], reverse=True)[:n]}
        return directors
    

    def __get_move_title__(self, imbd_id: str):
        id = None
        with open(self.file) as file:
            for line in file:
                if imbd_id in line.split(',')[1]:
                    id = line.split(',')[0]
                    break
        if id is None:
            print("iimdb id not found")
            return
        with open(self.moves_file) as file:
            for line in file:
                if id in line.split(',')[0]:
                    name = line.split(',')[1]
                    return name
        
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        budgets = dict()
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for film_data in big_list:
            if film_data[2][0] != None:
                budgets[self.__get_move_title__(film_data[0])] = int(film_data[2][0])

        budgets = {k: v for k ,v in sorted(budgets.items(), key=lambda x: x[1], reverse=True)[:n]}
        
        return budgets


    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
        profits = dict()
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for film_data in big_list:
            if film_data[2][0] != None and film_data[3][0] != None:
                profits[self.__get_move_title__(film_data[0])] = int(film_data[3][0]) - int(film_data[2][0])

        profits = {k: v for k ,v in sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n]}

        return profits
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
     Sort it by runtime descendingly.
        """
        runtimes = dict()
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for film_data in big_list:
            if film_data[4][0] != None:
                runtimes[self.__get_move_title__(film_data[0])] = int(film_data[4][0])

        return {k: v for k ,v in sorted(runtimes.items(), key=lambda x: x[1], reverse=True)[:n]}

        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies - do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        costs = dict()
        big_list = list()
        with open(self.dump_file) as dump_file:
            big_list = json.loads(dump_file.read())

        for film_data in big_list:
            if film_data[2][0] != None and film_data[4][0] != None:
                costs[self.__get_move_title__(film_data[0])] = round(int(film_data[2][0]) / int(film_data[4][0]), 2)

        return {k: v for k ,v in sorted(costs.items(), key=lambda x: x[1], reverse=True)[:n]}






def test_Links_useful_dict():
    useful_dict = Links.__useful_dict__('0114709')
    
    assert useful_dict == {'Director': ['John Lasseter'], 'Writers': ['John Lasseter', 'Pete Docter', 'Andrew Stanton'], 'Stars': ['Tom Hanks', 'Tim Allen', 'Don Rickles'], 'Nominated for 3 Oscars': ['29 wins & 24 nominations total'], 'Quotes': ['Woody', 'Buzz', 'Woody', 'Buzz', 'Woody'], 'Crazy credits': ['Приключения Флика (1998)', 'История игрушек 2 (1999)', 'Корпорация монстров (2001)', 'В поисках Немо (2003)'], 'Connections': ['Gamesmaster: Episode #5.9'], 'Soundtracks': ["You've Got a Friend in Me", 'Randy Newman', 'Randy Newman'], 'Release date': ['December 22, 1995 (Russia)'], 'Country of origin': ['United States'], 'Language': ['English'], 'Also known as': ['Toy Story'], 'Filming locations': ['Pixar Animation Studios - 1200 Park Avenue, Emeryville, California, USA'], 'Production companies': ['Walt Disney Pictures', 'Pixar Animation Studios'], 'Budget': [30000000], 'Gross US & Canada': [223225679], 'Opening weekend US & Canada': [29140617, 'Nov 26, 1995'], 'Gross worldwide': [394436586], 'Runtime': [81], 'Sound mix': ['Dolby Stereo', '(original version)', 'Spectra-Stereo', '(original version)', 'Dolby Digital'], 'Aspect ratio': ['1.78 : 1 / (high definition)']}

def test_Links_get_imdb_one():
    imdb_info = Links.get_imdb(['0113497'], ['Director', 'Release date', 'Runtime'])
    
    assert imdb_info == [['0113497', ['Joe Johnston'], ['March 6, 1996 (Russia)'], [104]]]

def test_Links_get_imdb_two():
    imdb_info = Links.get_imdb(['0114709', '0113497'], ['Director', 'Gross worldwide', 'Runtime'])

    assert imdb_info == [['0114709', ['John Lasseter'], [394436586], [81]], ['0113497', ['Joe Johnston'], [262821940], [104]]]

def test_Links_top_directors():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.top_directors(5) == {'Alfred Hitchcock': 11, 'Woody Allen': 8, 'Stanley Kubrick': 6, 'Frank Capra': 6, 'Rob Reiner': 5}
    assert links.top_directors(9) == {'Alfred Hitchcock': 11, 'Woody Allen': 8, 'Stanley Kubrick': 6, 'Frank Capra': 6, 'Rob Reiner': 5, 'Martin Scorsese': 5, 'Tony Scott': 5, 'John Carpenter': 5, 'James Cameron': 5}

def test_Links__get_move_title__():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.__get_move_title__('0114709') == 'Toy Story (1995)'
    assert links.__get_move_title__('0113228') == 'Grumpier Old Men (1995)'

def test_Links__dump_all_data__():
    links = Links('../datasets/ml-latest-small/links.csv')
    links.__dump_all_data__('test.json', 2)

    with open('comparator.json') as comparator:
        with open('test.json') as test_file:
            assert test_file.read() == comparator.read()



def test_Links_most_expensive():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.most_expensive(10) == {'Akira (1988)': 1100000000, 'Ghost in the Shell (Kôkaku kidôtai) (1995)': 330000000, 'Waterworld (1995)': 175000000, 'Germinal (1993)': 164000000, 'Cold Fever (Á köldum klaka) (1995)': 130000000, 'True Lies (1994)': 115000000, 'Terminator 2: Judgment Day (1991)': 102000000, 'Batman Forever (1995)': 100000000, '"Hunchback of Notre Dame': 100000000, 'Eraser (1996)': 100000000}

def test_Links_most_profitable():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.most_profitable(10) == {'Jurassic Park (1993)': 1041379926, '"Lion King': 934161373, 'E.T. the Extra-Terrestrial (1982)': 786807407, 'Star Wars: Episode IV - A New Hope (1977)': 764398507, 'Independence Day (a.k.a. ID4) (1996)': 742400891, 'Forrest Gump (1994)': 623226465, 'Star Wars: Episode V - The Empire Strikes Back (1980)': 532016086, 'Ghost (1990)': 483703557, 'Aladdin (1992)': 476050219, 'Home Alone (1990)': 458684675}

def test_Links_longest():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.longest(10) == {'Gone with the Wind (1939)': 238, 'Once Upon a Time in America (1984)': 229, 'Lawrence of Arabia (1962)': 227, 'Ben-Hur (1959)': 212, '"Godfather: Part II': 202, 'Giant (1956)': 201, "Schindler's List (1993)": 195, '"Right Stuff': 193, 'Nixon (1995)': 192, 'Wyatt Earp (1994)': 191}

def test_Links_top_cost_per_minute():
    links = Links('../datasets/ml-latest-small/links.csv')
    assert links.top_cost_per_minute(10) == {'Akira (1988)': 8870967.74, 'Ghost in the Shell (Kôkaku kidôtai) (1995)': 3975903.61, 'Cold Fever (Á köldum klaka) (1995)': 1566265.06, 'Waterworld (1995)': 1296296.3, '"Hunchback of Notre Dame': 1098901.1, 'Germinal (1993)': 1025000.0, 'Judge Dredd (1995)': 937500.0, 'Space Jam (1996)': 909090.91, 'Eraser (1996)': 869565.22, 'Batman Forever (1995)': 826446.28}





if __name__ == '__main__':
    links = Links('../datasets/ml-latest-small/links.csv')
    #links.__dump_all_data__('big_list.json', 1000)
    #xlinks.__convert_money__()
    links.__dump_all_data__('comparator.json', 2)

    print(links.most_expensive(10))
    print(links.most_profitable(10))
    print(links.longest(10))
    print(links.top_cost_per_minute(10))