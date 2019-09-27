import sys
import getopt
import csv

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts,args = getopt.getopt(argv, "hi:o:", [
                             "help", "input=", "output=", "task=", "propList=", "bin="])
    except getopt.GetoptError:
        print('-h,--help (for more information)')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(
                '1712713.py preprocess --input original.csv --output processed.csv --task remove --propList {id, name}')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        print('Input file is "', inputfile)
        print('Output file is "', outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
    
# def main():
#     inputfile="original.csv"
#     outputfile="processed.csv"
    
