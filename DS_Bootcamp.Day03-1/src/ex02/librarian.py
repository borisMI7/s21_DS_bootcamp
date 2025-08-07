import os
import subprocess

def installer():
    subprocess.run("\
        (echo 'beautifulsoup4\npytest' > req.txt)&&(pip install -r req.txt)&&(rm req.txt)\
    ", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sOut = subprocess.check_output(['pip', 'freeze']).decode("utf-8")
    print(sOut, end="")

    with open("requirements.txt", "w") as file:
        file.write(sOut)


def main():
    try:
        path = os.environ["VIRTUAL_ENV"]
    except Exception:
        print("Not in virtual env")
    else:
        if path.endswith('/DS_Bootcamp.Day03-1/src/ex02/gwynethl'):
            installer()
        else:
            print("Wrong env")


if __name__ == "__main__":
    main()