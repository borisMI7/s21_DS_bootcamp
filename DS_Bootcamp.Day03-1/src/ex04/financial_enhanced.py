from bs4 import BeautifulSoup
import requests
import sys

def find(field, table):
    for row in table.find_all('div', class_ = 'row lv-0 yf-t22klz'):
        item = row.find('div', class_ = 'column sticky yf-t22klz').text.strip()
        if item == field:
            tpl = tuple([div.text.strip() for div in row.find_all('div')][1+(field == "Total Revenue"):])
            return tpl
    raise Exception("Requested field does not exist")

def getHTML(ticker):
    link = f"https://finance.yahoo.com/quote/{ticker}/financials/"
    resp = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0'})
    txt = resp.text
    return txt

def main():
    if len(sys.argv) != 3:
        raise Exception("Incorrect number of arguments")

    txt = getHTML(sys.argv[1])
    soup = BeautifulSoup(txt, 'lxml')
    table = soup.find('div', class_ = 'tableBody yf-9ft13')

    if table == None:
        raise Exception("URL doesnt exist")

    print(find(sys.argv[2], table))


if __name__ == "__main__":
    main()