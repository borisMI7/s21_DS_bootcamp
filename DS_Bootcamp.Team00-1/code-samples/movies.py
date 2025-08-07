



class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = dict()
        with open(self.file_path) as file:
            for line in file:
                #date = re.search(r'(?<=\()\d\d\d\d(?=\))', line).group(0)
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
        with open(self.file_path) as file:
            #remove head of .csv
            file.readline()
            for line in file:
                line_genres = line.split(',')[-1].replace('\n', '').split('|')
                for genre in line_genres:
                    genres[genre] = genres.get(genre, 0) + 1

        return {k: v for k, v in sorted(genres.items(), key=lambda x: x[1], reverse=True)}

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """

        moves = dict()
        with open(self.file_path) as file:
            #remove head of .csv
            file.readline()
            for line in file:
                cnt_genres = len(line.split(',')[-1].replace('\n', '').split('|'))
                moves[line.split(',')[1]] = cnt_genres

        moves = {k: v for k, v in sorted(moves.items(), key=lambda x: x[1], reverse=True)}
        return dict(list(moves.items())[:n])


def test_Movies_dist_by_release():
    movies = Movies('../datasets/ml-latest-small/movies.csv')
    assert movies.dist_by_release() == {2002: 311, 2006: 295, 2001: 294, 2007: 284, 2000: 283, 2009: 282, 2003: 279, 2004: 279, 2014: 278, 1996: 276, 2015: 274, 2005: 273, 2008: 269, 1999: 263, 1997: 260, 1995: 259, 1998: 258, 2011: 254, 2010: 247, 2013: 239, 1994: 237, 2012: 233, 2016: 218, 1993: 198, 1992: 167, 1988: 165, 1987: 153, 1990: 147, 1991: 147, 2017: 147, 1989: 142, 1986: 139, 1985: 126, 1984: 101, 1981: 92, 1980: 89, 1982: 87, 1983: 83, 1979: 69, 1977: 63, 1973: 59, 1978: 59, 1965: 47, 1971: 47, 1974: 45, 1976: 44, 1964: 43, 1967: 42, 1968: 42, 1975: 42, 1966: 42, 2018: 41, 1962: 40, 1972: 39, 1963: 39, 1959: 37, 1960: 37, 1955: 36, 1969: 35, 1961: 34, 1970: 33, 1957: 33, 1958: 31, 1953: 30, 1956: 30, 1940: 25, 1949: 25, 1954: 23, 1942: 23, 1939: 23, 1946: 23, 1951: 22, 1950: 21, 1947: 20, 1948: 20, 1941: 18, 1936: 18, 1945: 17, 1937: 16, 1952: 16, 1944: 16, 1938: 15, 1931: 14, 1935: 13, 1933: 12, 1934: 11, 1943: 10, 1932: 9, 1927: 7, 1930: 5, 1926: 5, 1924: 5, 1929: 4, 1928: 4, 1925: 4, 1923: 4, 1916: 4, 1920: 2, 1922: 1, 1919: 1, 1921: 1, 1915: 1, 1917: 1, 1902: 1, 1903: 1, 1908: 1}

def test_Movies_dist_by_genres():
    movies = Movies('../datasets/ml-latest-small/movies.csv')
    assert movies.dist_by_genres() == {'Drama': 4361, 'Comedy': 3756, 'Thriller': 1894, 'Action': 1828, 'Romance': 1596, 'Adventure': 1263, 'Crime': 1199, 'Sci-Fi': 980, 'Horror': 978, 'Fantasy': 779, 'Children': 664, 'Animation': 611, 'Mystery': 573, 'Documentary': 440, 'War': 382, 'Musical': 334, 'Western': 167, 'IMAX': 158, 'Film-Noir': 87, '(no genres listed)': 34}
 
def test_Movies_most_genres():
    movies = Movies('../datasets/ml-latest-small/movies.csv')
    assert movies.most_genres(10) == {'Rubber (2010)': 10, 'Patlabor: The Movie (Kidô keisatsu patorebâ: The Movie) (1989)': 8, 'Mulan (1998)': 7, 'Who Framed Roger Rabbit? (1988)': 7, 'Osmosis Jones (2001)': 7, 'Interstate 60 (2002)': 7, 'Robots (2005)': 7, 'Pulse (2006)': 7, 'Aqua Teen Hunger Force Colon Movie Film for Theaters (2007)': 7, 'Enchanted (2007)': 7}



if __name__ == '__main__':
    movies = Movies('../datasets/ml-latest-small/movies.csv')
    print(movies.dist_by_genres())
    print(movies.most_genres(10))
