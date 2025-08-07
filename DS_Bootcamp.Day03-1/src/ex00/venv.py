import os


def main():
    path = os.environ["VIRTUAL_ENV"]
    print(f"Your current virtual env is {path}")

if __name__ == "__main__":
    main()