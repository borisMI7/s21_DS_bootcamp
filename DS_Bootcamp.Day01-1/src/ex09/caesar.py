import sys


def main():
    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments")
    elif sys.argv[1] == "encode":
        print(encode(sys.argv[2], int(sys.argv[3])))
    elif sys.argv[1] == "decode":
        print(encode(sys.argv[2], -int(sys.argv[3])))


def shift_ch(ch: int, shift: int) -> int:
    ch += shift
    return ((ch - 97) % 26) + 97


def encode(string: str, shift: int) -> str:
    string = list(string)
    for i in range(0, len(string)):
        ch = ord(string[i])
        if ch > 127:
            raise Exception("The script does not support your language yet")
        elif 96 < ch < 123:
            string[i] = chr(shift_ch(ch, shift))
    return "".join(string)


if __name__ == "__main__":
    main()
