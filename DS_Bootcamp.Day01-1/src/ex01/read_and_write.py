def start():
    file = open("../../datasets/ds.csv")
    new_file = open("ds.tsv", "w")

    data = file.read().split("\n")

    for line in data:
        tokenized_line = []
        split_line(line, tokenized_line)
        new_file.write("\t".join(tokenized_line) + "\n")

    file.close()
    new_file.close()


def split_line(line: str, tokenized_line: list) -> list:

    if len(line) == 0:
        return tokenized_line

    if line[0] == '"' and line.find(",") != -1:
        idx = line.find('",')
        tokenized_line.append(line[0: idx + 1])
        split_line(line[idx + 2:], tokenized_line)
        
    elif line.find(",") != -1:
        idx = line.find(",")
        tokenized_line.append(line[0:idx])
        split_line(line[idx + 1:], tokenized_line)

    else:
        tokenized_line.append(line)
        return tokenized_line


if __name__ == "__main__":
    start()
