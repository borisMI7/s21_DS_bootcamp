import sys


def start():
    if len(sys.argv) != 2:
        exit(1)
    print_name_and_price(sys.argv[1])


def print_name_and_price(sym: str):

    sym = sym.upper()

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
    if sym in STOCKS:
        print(find_by_value(COMPANIES, sym), STOCKS[sym])
    else:
        print("Unknown ticker")


def find_by_value(d: dict, target):
    for key, value in d.items():
        if value == target:
            return key


if __name__ == "__main__":
    start()
