import sys
import os

def main():
    inputfile = "countries.txt"
    outputfile = "output.txt"
    with open(outputfile, "r") as f:
        lines = f.readlines()
        print(lines)
    with open(outputfile, "w") as f:
        for line in lines:
            string = line.strip("\n")
            if string != "name=name":
                    f.write(line)


if __name__ == '__main__':
    main()
        