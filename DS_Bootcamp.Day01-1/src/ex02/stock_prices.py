import sys


def start():
    if len(sys.argv) != 2:
        exit(1)
    print(get_price(sys.argv[1]))


def get_price(name: str):
    name = name.capitalize()
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
    if name in COMPANIES:
        return STOCKS[COMPANIES[name]]
    else:
        return "Unknown company"


if __name__ == "__main__":
    start()
