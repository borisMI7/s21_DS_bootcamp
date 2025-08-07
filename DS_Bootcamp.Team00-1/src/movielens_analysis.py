import collections
import datetime
import requests
import bs4
import json
import pytest
import re
from unittest.mock import mock_open



class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def lines_generator(self, path_to_the_file):
        try:
            with open(path_to_the_file, "r") as file:
                next(file)
                for line in file:
                    yield line.split(",")
        except FileNotFoundError:
            raise Exception("File not found")


    def check_file_structure(self):
        self.file_content = self.lines_generator(self.path_to_the_file)
        for line in self.file_content:
            if len(line) != 4:
                raise Exception("incorrect file structure")
            try:
                int(line[0])
                int(line[1])
                float(line[2])
                float(line[3])
            except ValueError:
                raise Exception("incorrect file data")

    def __init__(self, path_to_the_file, path_to_the_movies):
        self.path_to_the_file = path_to_the_file
        self.check_file_structure()
        self.movies = Ratings.Movies(path_to_the_file, self.lines_generator, path_to_the_movies)
        self.users = Ratings.Users(path_to_the_file, self.lines_generator, path_to_the_movies)

    class Movies:
        def __init__(self, path_to_the_file, lines_generator, path_to_the_movies):
            self.lines_generator = lines_generator
            self.path_to_the_file = path_to_the_file
            self.path_to_the_movies = path_to_the_movies

        @staticmethod
        def line_to_year(line):
            return int(datetime.datetime.fromtimestamp(int(line[3])).strftime("%Y"))


        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            self.file_content = self.lines_generator(self.path_to_the_file)
            year_counter = collections.Counter([self.line_to_year(line) for line in self.file_content])
            ratings_by_year = dict(year_counter)
            return {year:ratings_by_year[year] for year in sorted(ratings_by_year)}

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            self.file_content = self.lines_generator(self.path_to_the_file)
            rating_counter = collections.Counter([float(line[2]) for line in self.file_content])

            ratings_distribution = dict(rating_counter)
            return {rating:ratings_distribution[rating] for rating in sorted(ratings_distribution)}

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
     Sort it by numbers descendingly.
            """
            self.file_content = self.lines_generator(self.path_to_the_file)
            id_counter = collections.Counter([int(line[1]) for line in self.file_content])
            top_id = dict(id_counter.most_common(n))

            movies_content = self.lines_generator(self.path_to_the_movies)
            top_movies = {}
            for line in movies_content:
                if int(line[0]) in top_id.keys():
                    top_movies[line[1]] = top_id[int(line[0])]
            return top_movies

        def get_ratings(self):
            self.file_content = self.lines_generator(self.path_to_the_file)
            movie_ratings = {}
            for line in self.file_content:
                id = int(line[1])
                rating = float(line[2])
                if id in movie_ratings.keys():
                    movie_ratings[id].append(rating)
                else:
                    movie_ratings[id] = [rating]
            return movie_ratings

        def count_average(self, list):
            return sum(list)/len(list)

        def count_median(self, list):
            list.sort()
            if len(list) == 1:
                return list[0]
            elif len(list)%2 != 0:
                return list[len(list)//2]
            else:
                return self.count_average(list[len(list)//2 - 1:len(list)//2 + 1])

        def count_variance(self, list):
            if len(list) == 1:
                return 0
            mean = self.count_average(list)
            return sum([(x - mean)**2 for x in list])/(len(list)-1)

        def top_by_ratings(self, n, metric="average"):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = self.get_ratings()

            movie_metric = {}
            for key, value in movie_ratings.items():
                if(metric == "average"):
                    movie_metric[key] = round(self.count_average(value), 2)
                elif(metric == "median"):
                    movie_metric[key] = round(self.count_median(value), 2)
                else:
                    raise Exception("incorrect metric name:", metric)

            top_movies = {key:value for key, value in sorted(movie_metric.items(), key = lambda item: item[1], reverse=True)}
            top = {key: value for key, value in list(top_movies.items())[:n]}

            movies_content = self.lines_generator(self.path_to_the_movies)
            top_movies = {}
            for line in movies_content:
                if int(line[0]) in top.keys():
                    top_movies[line[1]] = top[int(line[0])]
            return top_movies



        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            movies_rating = self.get_ratings()

            movie_variance = {}
            for key, value in movies_rating.items():
                movie_variance[key] = round(self.count_variance(value), 2)

            top_movies = {key:value for key, value in sorted(movie_variance.items(), key = lambda item: item[1], reverse=True)}
            top = {key: value for key, value in list(top_movies.items())[:n]}
            movies_content = self.lines_generator(self.path_to_the_movies)
            top_movies = {}
            for line in movies_content:
                if int(line[0]) in top.keys():
                    top_movies[line[1]] = top[int(line[0])]
            return top_movies

    class Users(Movies):
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def number_of_ratings(self):
            self.file_content = self.lines_generator(self.path_to_the_file)
            return dict(collections.Counter([int(line[0]) for line in self.file_content]).most_common())

        def get_user_ratings(self):
            self.file_content = self.lines_generator(self.path_to_the_file)
            user_ratings = {}
            for line in self.file_content:
                id = int(line[0])
                rating = float(line[2])
                if id in user_ratings.keys():
                    user_ratings[id].append(rating)
                else:
                    user_ratings[id] = [rating]
            return user_ratings

        def users_by_metric(self, metric = "average"):
            user_ratings = self.get_user_ratings()
            user_metrics = {}
            for key, value in user_ratings.items():
                if metric == "average":
                    user_metrics[key] = round(self.count_average(value), 2)
                elif metric == "median":
                    user_metrics[key] = round(self.count_median(value), 2)

            user_metrics = {key:value for key, value in sorted(user_metrics.items(), key = lambda item: item[1], reverse=True)}
            return user_metrics

        def top_users_by_varince(self, n):
            user_ratings = self.get_user_ratings()
            user_variance = {}
            for key, value in user_ratings.items():
                user_variance[key] = round(self.count_variance(value), 2)

            top_users = {key:value for key, value in sorted(user_variance.items(), key = lambda item: item[1], reverse=True)}
            return {key: value for key, value in list(top_users.items())[:n]}

class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        try:
            with open(path_to_the_file, "r") as file:
                self.tags = [line.split(",")[2].strip() for line in file.readlines()[1:]]
        except FileNotFoundError:
            raise Exception("file not found")
        except IndexError:
            raise Exception("incorrect file structure")


    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
 where the keys are tags and the values are the number of words inside the tag.
 Drop the duplicates. Sort it by numbers descendingly.
        """
        sorted_tags = sorted(set(self.tags), key = lambda tag: len(tag.split(" ")), reverse = True)
        big_tags = {key:len(key.split(" ")) for key in sorted_tags[0:n]}

        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = sorted(set(self.tags), key = lambda tag: len(tag), reverse = True)[0:n]
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """

        most_words = self.most_words(n)
        longest = self.longest(n)

        big_tags = list(set(most_words) & set(longest))

        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """

        cnt = collections.Counter(self.tags).most_common(n)
        popular_tags = dict(cnt)

        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """

        tags_with_word = sorted(list(set(filter(lambda tag: word in tag, self.tags))))
        return tags_with_word

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file='../datasets/links.csv', path_to_movies='../datasets/movies.csv', dump_file_path='../datasets/big_list.json'):
        """
        Put here any fields that you think you will need.
        """
        self.file = path_to_the_file
        self.movies_file = path_to_movies
        self.dump_file = dump_file_path

        with open(path_to_the_file) as file:
            self.data = file.readlines()

        with open(path_to_movies) as movies_file:
            for num in range(len(self.data)):
                self.data[num] = self.data[num][:-1] + ',' + movies_file.readline()



    def __dump_all_data__(self, dump_file_path, max_lines = 10000):
        big_list = list()
        fields = ['Director', 'Budget', 'Gross worldwide', 'Runtime']

        line_cnt = 1
        for line in self.data[1:]:
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
        page.raise_for_status()

        soup = bs4.BeautifulSoup(page.text, 'html.parser')



        #найдем все теги с списками на странице и пробежимся по ним
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
        for line in self.data:
            if imbd_id in line.split(',')[1]:
                return line.split(',')[4]
        return None


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

class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file
        with open(path_to_the_file) as file:
            self.data = file.readlines()

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = dict()
        for line in self.data:
            match = re.search(r'(?<=\()\d{4}(?=\))', line)
            if match:
                date = int(match.group(0))
                release_years[date] = release_years.get(date, 0)+1


        return {k: v for k, v in sorted(release_years.items(), key=lambda x: x[1], reverse=True)}

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        genres = dict()
        for line in self.data:
            line_genres = line.split(',')[-1].replace('\n', '').split('|')
            for genre in line_genres:
                genres[genre] = genres.get(genre, 0) + 1

        genres = {k: v for k, v in sorted(genres.items(), key=lambda x: x[1], reverse=True)}
        genres.pop('genres', None)
        return genres

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        moves = dict()
        for line in self.data:
            cnt_genres = len(line.split(',')[-1].replace('\n', '').split('|'))
            moves[line.split(',')[1]] = cnt_genres

        moves = {k: v for k, v in sorted(moves.items(), key=lambda x: x[1], reverse=True)}
        return dict(list(moves.items())[:n])

class Test():

    @pytest.fixture
    def create_tags_correct(self, mocker):
        mock_file = mock_open(read_data =
            "userId, movieId, tag, timestamp\n\
            1, 1, a, 0\n\
            1, 1, a, 0\n\
            1, 1, a, 0\n\
            1, 1, ba, 1323456464\n\
            1, 1, ba, 1323456464\n\
            1, 1, word1 word2, 1627279008\n\
            1, 1, word1 word2 word3, 1627279008"
        )
        mocker.patch("builtins.open", mock_file)
        tags = Tags("input.txt")
        return tags


    @pytest.fixture
    def create_ratings_correct(self, mocker):
        '''
        1 фильм - оценили 1 раз, 1 пользователь, в 1970
        2 фильм - оценили 2 раза, 1, 2 пользователь, в 2011 году
        3 фильм - оценили 3 раза, 1, 2, 3 пользователь, в 2021 году
        '''

        r = "userId, movieId, rating, timestamp\n\
        1, 1, 1.0, 0\n\
        1, 2, 1.0, 1323456464\n\
        2, 2, 2.0, 1323456464\n\
        1, 3, 1.0, 1627279008\n\
        2, 3, 2.0, 1627279008\n\
        3, 3, 3.0, 1627279008"

        m = "movieId,title,genres\n\
        1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy\n\
        2,Jumanji (1995),Adventure|Children|Fantasy\n\
        3,Grumpier Old Men (1995),Comedy|Romance"

        mock_files = {
                "input.txt": r,
                "../datasets/movies.csv": m
            }
        def mock_file_open(filename, *args, **kwargs):
            if filename in mock_files:
                return mock_open(read_data=mock_files[filename]).return_value
            raise FileNotFoundError(f"Mock file {filename} not found")

        mocker.patch("builtins.open", side_effect=mock_file_open)

        ratings = Ratings("input.txt", "../datasets/movies.csv")
        return ratings

    def test_ratings_init(self, create_ratings_correct):
        assert create_ratings_correct.path_to_the_file == "input.txt"
        assert type(create_ratings_correct.movies) is Ratings.Movies
        assert type(create_ratings_correct.users) is Ratings.Users


    def test_line_to_year(self):
        # Input: Unix epoch start timestamp (0)
        line = ["", "", "", "0"]
        assert Ratings.Movies.line_to_year(line) == 1970

        # Input: Known timestamp from 2011 (1323456464)
        line = ["", "", "", "1323456464"]
        assert Ratings.Movies.line_to_year(line) == 2011

        # Input: Sample timestamp from 2021 (1627279008)
        line = ["", "", "", "1627279008"]
        assert Ratings.Movies.line_to_year(line) == 2021

    def test_movie_dist_by_year(self, create_ratings_correct):
        assert create_ratings_correct.movies.dist_by_year() == {1970:1, 2011:2, 2021:3}

    def test_dist_by_ratings(self, create_ratings_correct):
        assert create_ratings_correct.movies.dist_by_rating() == {1.0:3, 2.0:2, 3.0:1}

    def test_top_by_num_of_ratings(self, create_ratings_correct):
        assert create_ratings_correct.movies.top_by_num_of_ratings(3) == {'Grumpier Old Men (1995)':3, 'Jumanji (1995)':2, 'Toy Story (1995)':1}

    def test_top_by_ratings(self, create_ratings_correct):
        assert create_ratings_correct.movies.top_by_ratings(3, "average") == {'Grumpier Old Men (1995)': 2.00, 'Jumanji (1995)': 1.50, 'Toy Story (1995)': 1}
        assert create_ratings_correct.movies.top_by_ratings(2, "average") == {'Grumpier Old Men (1995)': 2.00, 'Jumanji (1995)': 1.50}
        assert create_ratings_correct.movies.top_by_ratings(3, "median") == {'Grumpier Old Men (1995)': 2.00, 'Jumanji (1995)': 1.50, 'Toy Story (1995)': 1}

    def test_top_controversial(self, create_ratings_correct):
        assert create_ratings_correct.movies.top_controversial(3) == {'Grumpier Old Men (1995)': 1.00, 'Jumanji (1995)': 0.5, 'Toy Story (1995)':0}

    def test_number_of_ratings(self, create_ratings_correct):
        assert create_ratings_correct.users.number_of_ratings() == {1:3, 2:2, 3:1}

    def test_get_user_ratings(self, create_ratings_correct):
        assert create_ratings_correct.users.get_user_ratings() == {1:[1, 1, 1], 2:[2, 2], 3:[3]}

    def test_users_by_metric(self, create_ratings_correct):
        assert create_ratings_correct.users.users_by_metric(metric = "average") == {3:3.00, 2:2.00, 1:1.00}
        assert create_ratings_correct.users.users_by_metric(metric = "median") ==  {3:3.00, 2:2.00, 1:1.00}

    def test_top_users_by_varince(self, create_ratings_correct):
        assert create_ratings_correct.users.top_users_by_varince(3) == {1: 0, 2: 0, 3:0}

    def test_most_words(self, create_tags_correct):
        assert create_tags_correct.most_words(2) == {'word1 word2 word3':3, 'word1 word2':2}

    def test_longest(self, create_tags_correct):
        assert create_tags_correct.longest(2) == ['word1 word2 word3', 'word1 word2']

    def test_most_words_and_longest(self, create_tags_correct):
        assert set(create_tags_correct.most_words_and_longest(2)) == set(['word1 word2', 'word1 word2 word3'])

    def test_most_popular(self, create_tags_correct):
        assert create_tags_correct.most_popular(2) == {'a':3, 'ba':2}

    def test_tags_with(self, create_tags_correct):
        print(create_tags_correct.tags_with('word1'))
        assert create_tags_correct.tags_with('a') ==  ['a', 'ba']

    @staticmethod
    def test_Movies_dist_by_release():
        movies = Movies('../datasets/movies.csv')
        assert movies.dist_by_release() == {2002: 311, 2006: 295, 2001: 294, 2007: 284, 2000: 283, 2009: 282, 2003: 279, 2004: 279, 2014: 278, 1996: 276, 2015: 274, 2005: 273, 2008: 269, 1999: 263, 1997: 260, 1995: 259, 1998: 258, 2011: 254, 2010: 247, 2013: 239, 1994: 237, 2012: 233, 2016: 218, 1993: 198, 1992: 167, 1988: 165, 1987: 153, 1990: 147, 1991: 147, 2017: 147, 1989: 142, 1986: 139, 1985: 126, 1984: 101, 1981: 92, 1980: 89, 1982: 87, 1983: 83, 1979: 69, 1977: 63, 1973: 59, 1978: 59, 1965: 47, 1971: 47, 1974: 45, 1976: 44, 1964: 43, 1967: 42, 1968: 42, 1975: 42, 1966: 42, 2018: 41, 1962: 40, 1972: 39, 1963: 39, 1959: 37, 1960: 37, 1955: 36, 1969: 35, 1961: 34, 1970: 33, 1957: 33, 1958: 31, 1953: 30, 1956: 30, 1940: 25, 1949: 25, 1954: 23, 1942: 23, 1939: 23, 1946: 23, 1951: 22, 1950: 21, 1947: 20, 1948: 20, 1941: 18, 1936: 18, 1945: 17, 1937: 16, 1952: 16, 1944: 16, 1938: 15, 1931: 14, 1935: 13, 1933: 12, 1934: 11, 1943: 10, 1932: 9, 1927: 7, 1930: 5, 1926: 5, 1924: 5, 1929: 4, 1928: 4, 1925: 4, 1923: 4, 1916: 4, 1920: 2, 1922: 1, 1919: 1, 1921: 1, 1915: 1, 1917: 1, 1902: 1, 1903: 1, 1908: 1}

    @staticmethod
    def test_Movies_dist_by_genres():
        movies = Movies('../datasets/movies.csv')
        assert movies.dist_by_genres() == {'Drama': 4361, 'Comedy': 3756, 'Thriller': 1894, 'Action': 1828, 'Romance': 1596, 'Adventure': 1263, 'Crime': 1199, 'Sci-Fi': 980, 'Horror': 978, 'Fantasy': 779, 'Children': 664, 'Animation': 611, 'Mystery': 573, 'Documentary': 440, 'War': 382, 'Musical': 334, 'Western': 167, 'IMAX': 158, 'Film-Noir': 87, '(no genres listed)': 34}

    @staticmethod
    def test_Movies_most_genres():
        movies = Movies('../datasets/movies.csv')
        assert movies.most_genres(10) == {'Rubber (2010)': 10, 'Patlabor: The Movie (Kidô keisatsu patorebâ: The Movie) (1989)': 8, 'Mulan (1998)': 7, 'Who Framed Roger Rabbit? (1988)': 7, 'Osmosis Jones (2001)': 7, 'Interstate 60 (2002)': 7, 'Robots (2005)': 7, 'Pulse (2006)': 7, 'Aqua Teen Hunger Force Colon Movie Film for Theaters (2007)': 7, 'Enchanted (2007)': 7}


    @staticmethod
    def test_Links_useful_dict():
        useful_dict = Links.__useful_dict__('0114709')

        assert useful_dict == {'Director': ['John Lasseter'], 'Writers': ['John Lasseter', 'Pete Docter', 'Andrew Stanton'], 'Stars': ['Tom Hanks', 'Tim Allen', 'Don Rickles'], 'Nominated for 3 Oscars': ['29 wins & 24 nominations total'], 'Quotes': ['Woody', 'Buzz', 'Woody', 'Buzz', 'Woody'], 'Crazy credits': ['Приключения Флика (1998)', 'История игрушек 2 (1999)', 'Корпорация монстров (2001)', 'В поисках Немо (2003)'], 'Connections': ['Gamesmaster: Episode #5.9'], 'Soundtracks': ["You've Got a Friend in Me", 'Randy Newman', 'Randy Newman'], 'Release date': ['December 22, 1995 (Russia)'], 'Country of origin': ['United States'], 'Language': ['English'], 'Also known as': ['Toy Story'], 'Filming locations': ['Pixar Animation Studios - 1200 Park Avenue, Emeryville, California, USA'], 'Production companies': ['Walt Disney Pictures', 'Pixar Animation Studios'], 'Budget': [30000000], 'Gross US & Canada': [223225679], 'Opening weekend US & Canada': [29140617, 'Nov 26, 1995'], 'Gross worldwide': [394436586], 'Runtime': [81], 'Sound mix': ['Dolby Stereo', '(original version)', 'Spectra-Stereo', '(original version)', 'Dolby Digital'], 'Aspect ratio': ['1.78 : 1 / (high definition)']}

    @staticmethod
    def test_Links_get_imdb_one():
        imdb_info = Links.get_imdb(['0113497'], ['Director', 'Release date', 'Runtime'])
        print(imdb_info)
        assert imdb_info == [['0113497', ['Joe Johnston'], ['March 6, 1996 (Russia)'], [104]]]

    @staticmethod
    def test_Links_get_imdb_two():
        imdb_info = Links.get_imdb(['0114709', '0113497'], ['Director', 'Gross worldwide', 'Runtime'])

        assert imdb_info == [['0114709', ['John Lasseter'], [394436586], [81]], ['0113497', ['Joe Johnston'], [262821940], [104]]]

    @staticmethod
    def test_Links_top_directors():
        links = Links('../datasets/links.csv')
        assert links.top_directors(5) == {'Alfred Hitchcock': 11, 'Woody Allen': 8, 'Stanley Kubrick': 6, 'Frank Capra': 6, 'Rob Reiner': 5}
        assert links.top_directors(9) == {'Alfred Hitchcock': 11, 'Woody Allen': 8, 'Stanley Kubrick': 6, 'Frank Capra': 6, 'Rob Reiner': 5, 'Martin Scorsese': 5, 'Tony Scott': 5, 'John Carpenter': 5, 'James Cameron': 5}

    @staticmethod
    def test_Links__get_move_title__():
        links = Links('../datasets/links.csv')
        assert links.__get_move_title__('0114709') == 'Toy Story (1995)'
        assert links.__get_move_title__('0113228') == 'Grumpier Old Men (1995)'

    @staticmethod
    def test_Links__dump_all_data__():
        links = Links('../datasets/links.csv')
        links.__dump_all_data__('test.json', 2)

        with open('../datasets/comparator.json') as comparator:
            with open('test.json') as test_file:
                assert test_file.read() == comparator.read()

    @staticmethod
    def test_Links__convert_money__():
        links = Links('../datasets/links.csv', '../datasets/movies.csv', 'test.json')
        links.__dump_all_data__('test.json', 2)
        links.__convert_money__()

        with open('../datasets/comparator.json') as comparator:
            with open('test.json') as test_file:
                assert test_file.read() == comparator.read()


    @staticmethod
    def test_Links_most_expensive():
        links = Links('../datasets/links.csv')
        assert links.most_expensive(10) == {'Akira (1988)': 1100000000, 'Ghost in the Shell (Kôkaku kidôtai) (1995)': 330000000, 'Waterworld (1995)': 175000000, 'Germinal (1993)': 164000000, 'Cold Fever (Á köldum klaka) (1995)': 130000000, 'True Lies (1994)': 115000000, 'Terminator 2: Judgment Day (1991)': 102000000, 'Batman Forever (1995)': 100000000, '"Hunchback of Notre Dame': 100000000, 'Eraser (1996)': 100000000}

    @staticmethod
    def test_Links_most_profitable():
        links = Links('../datasets/links.csv')
        assert links.most_profitable(10) == {'Jurassic Park (1993)': 1041379926, '"Lion King': 934161373, 'E.T. the Extra-Terrestrial (1982)': 786807407, 'Star Wars: Episode IV - A New Hope (1977)': 764398507, 'Independence Day (a.k.a. ID4) (1996)': 742400891, 'Forrest Gump (1994)': 623226465, 'Star Wars: Episode V - The Empire Strikes Back (1980)': 532016086, 'Ghost (1990)': 483703557, 'Aladdin (1992)': 476050219, 'Home Alone (1990)': 458684675}

    @staticmethod
    def test_Links_longest():
        links = Links('../datasets/links.csv')
        assert links.longest(10) == {'Gone with the Wind (1939)': 238, 'Once Upon a Time in America (1984)': 229, 'Lawrence of Arabia (1962)': 227, 'Ben-Hur (1959)': 212, '"Godfather: Part II': 202, 'Giant (1956)': 201, "Schindler's List (1993)": 195, '"Right Stuff': 193, 'Nixon (1995)': 192, 'Wyatt Earp (1994)': 191}

    @staticmethod
    def test_Links_top_cost_per_minute():
        links = Links('../datasets/links.csv')
        assert links.top_cost_per_minute(10) == {'Akira (1988)': 8870967.74, 'Ghost in the Shell (Kôkaku kidôtai) (1995)': 3975903.61, 'Cold Fever (Á köldum klaka) (1995)': 1566265.06, 'Waterworld (1995)': 1296296.3, '"Hunchback of Notre Dame': 1098901.1, 'Germinal (1993)': 1025000.0, 'Judge Dredd (1995)': 937500.0, 'Space Jam (1996)': 909090.91, 'Eraser (1996)': 869565.22, 'Batman Forever (1995)': 826446.28}

