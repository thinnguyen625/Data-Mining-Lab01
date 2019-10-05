import sys
import parser
import csv


def process_file_text():
    with open("countries.txt", "r",encoding="utf8") as fi:
        with open("output.csv", 'w',encoding="utf8",newline='') as writeFile:
            csv_writer = csv.writer(writeFile)
            i = 0
            t = 0
            result = []
            data = []
            while True:
                line = fi.readline()
                if line == '' or line == None:
                    break
                if i < 8:
                    temp = line.strip('\n')
                    temp = temp.split('=')
                    result.append(temp[0])
                    if i == 7:
                        csv_writer.writerow(result)
                else:
                    temp = line.strip('\n')
                    temp = temp.split('=')
                    if temp[0] == result[0]:
                        t+=1
                        if t == 2:
                            csv_writer.writerow(data)
                            t=1
                        data = [temp[1],'','','','','','','']    
                    else:
                        tempIndex = result.index(temp[0])
                        data[tempIndex] = temp[1]                   
                i += 1
            writeFile.close()
    fi.close()

def main():
    process_file_text()

if __name__ == '__main__':
    main()
    

