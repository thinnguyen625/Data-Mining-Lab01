import sys
import getopt
import csv
import re
# import pandas as pd

# def main(argv):
#     inputfile = ''
#     outputfile = ''
#     try:
#         opts,args = getopt.getopt(argv, "hi:o:", [
#                              "help", "input=", "output=", "task=", "propList=", "bin="])
#     except getopt.GetoptError:
#         print('-h,--help (for more information)')
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt in ('-h', "--help"):
#             print(
#                 '1712713.py preprocess --input original.csv --output processed.csv --task remove --propList {id, name}')
#             sys.exit()
#         elif opt in ("-i", "--input"):
#             inputfile = arg
#         elif opt in ("-o", "--output"):
#             outputfile = arg
#         print('Input file is "', inputfile)
#         print('Output file is "', outputfile)


# if __name__ == "__main__":
#     main(sys.argv[1:])

def main():
    file_name_in = 'original.csv'
    file_name_out = "processed.csv"
    input_filedname = "passenger_numbers"
    data = readFieldInFile(file_name_in,input_filedname)
    dataFloat=data.convertDataToFloat()
    dataMinMax=zScoreNorm(dataFloat)
    dataMinMax.insert(0,input_filedname)
    writeFieldInFile(file_name_out,dataMinMax)
    data.clear()
    del data
   
    

class Attribute:
    def __init__(self,name,data):
        self.name=name
        self.data=data
    def convertDataToFloat(self):
        result=[]
        for i in self.data:
            if checkNumber(i):
              result.append(float(i))
            else: continue
        if len(result)>0:
            return result
        else: return None
    def appendData(self,param):
        self.data.append(param)
        return True 
    def clear(self):
        del self.name
        self.data.clear()
        del self.data
    
def delete_missing_value()
def checkNumber(x):
     result= re.search('(^[0-9])+(.{0})|(.{1})[0-9]*',x)
     if result:
         return True
     else: return False
def writeFieldInFile(fileOutput, data):
    if data:
        with open(fileOutput, mode='w',newline='') as writeFile:
            csv_writer = csv.writer(writeFile)
            convertFloatToString(data)
            for i in data:
                csv_writer.writerow([i])
        writeFile.close()
        return True
    return None
def convertFloatToString(data):
    for i in range(0,len(data)):
        if type(data[i])!= str:
            data[i]=repr(data[i])
    return data


def readFieldInFile(fileInput, fieldName):
    with open(fileInput,'r') as readFile:
        csv_reader = csv.DictReader(readFile)
        result = Attribute(fieldName,[])
        for row in csv_reader:
            result.appendData(row[fieldName])
    readFile.close()
    return result
        

def minMaxNorm(data, new_range=[0, 1]):  # hàm chuẩn hóa min max
    """Min-Max normalization fuction
         Parameters:   
             data : a list values of an numeric attribute 𝐴 that need Min-Max normalization
             new_range: [New_Min,New_Max]  default value is [0,1] if nothing value passed
       Return: An list hold all values that are normalized"""  # day la phan mo ta ham

    min_num = min(data)
    max_num = max(data)
    result = []  # mang chua kq tính từng dòng dữ liệu
    for i in data:
        # cong thuc tinh trong slide
        vi = ((i-min_num)/(max_num-min_num)) * \
            (new_range[1]-new_range[0])+new_range[1]
        result.append(vi)
    return result


def zScoreNorm(data):  # hàm chuẩn hóa Z-scores
    """Z-score normalization fuction
         Parameters:  data : a list values of an numeric attribute 𝐴 that need Z-score normalization
       Return an list hold all values that are normalized"""

    result = []
    d_mean = mean(data)
    d_stddev = stddev(data)  # độ lệch chuẩn
    for i in data:
        vi = (i-d_mean)/d_stddev
        result.append(vi)
    return result


def mean(data):  # hàm tính trung bình
    "Return the sample arithmetic mean of data"
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n)


def variance(data):  # hàm tính phương sai
    "Return variance of sequence data"
    d_mean = mean(data)
    d_sum = 0
    n = len(data)
    for i in data:
        d_sum = d_sum + (i-d_mean)**2
    return d_sum/float(n-1)


def stddev(data):
    "Return standard deviation of sequence data."
    return (variance(data))**0.5


if __name__ == '__main__':
    main()
    exit()
