import sys


def main():
    if len(sys.argv) == 2:
        string = sys.argv[1]
        string_list = string.split(sep=",")
        for item in string_list:
            item = item.strip()
            result = process_item(item)
            if result != None:
                print(result)


def process_item(item: str):
    COMPANIES = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Netflix": "NFLX",
        "Tesla": "TSLA",
        "Nokia": "NOK",
    }
    STOCKS = {
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
        "NOK": 3.37,
    }

    if item.capitalize() in COMPANIES.keys():
        item = item.capitalize()
        return item + " stock price " + str(STOCKS[COMPANIES[item]])

    elif item.upper() in COMPANIES.values():
        item = item.upper()
        for key in COMPANIES.keys():
            if COMPANIES[key] == item:
                return item + " is a ticker symbol for " + key

    elif item != "":
        return item + " is an unknown company or an unknown ticker symbol"


if __name__ == "__main__":
    main()
