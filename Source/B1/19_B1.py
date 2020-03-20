import sys
import argparse
import csv
import re


class Attribute:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def convertDataToFloat(self):
        result = []
        lenValid = 0
        for i in self.data:
            if checkNumber(i):
                result.append(float(i))
                lenValid += 1
            else:
                result.append(i)
        if lenValid > 0:
            return result
        else:
            return None

    def convertToOutput(self):
        result = [[self.name]]
        for i in self.data:
            result.append([i])
        return result

    def appendData(self, param):
        self.data.append(param)
        return True

    def clear(self):
        del self.name
        self.data.clear()
        del self.data


def rangeValid(field):
    if field:
        for i in field:
            if i != '':
                minField = i
                maxField = i
                break

        for i in range(1, len(field)):
            if field[i] != '':
                if field[i] > maxField:
                    maxField = field[i]
                elif field[i] < minField:
                    minField = field[i]
        return maxField-minField
    return None


def minValid(field):
    if field:
        for i in field:
            if i != '':
                result = i
                break

        for i in range(1, len(field)):
            if field[i] != '':
                if field[i] < result:
                    result = field[i]
        return result
    return None


def maxValid(field):
    if field:
        for i in field:
            if i != '':
                result = i
                break
        for i in range(1, len(field)):
            if field[i] != '':
                if field[i] > result:
                    result = field[i]
        return result
    return None


def checkNumber(x):
    if x == '':
        return False
    for i in x:
        if i not in '0123456789.':
            return False
    return True


def writeFieldInFile(fileOutput, data):
    if data:
        with open(fileOutput, mode='w', newline='') as writeFile:
            csv_writer = csv.writer(writeFile)
            outputData = modifyDataToOutput(data)
            csv_writer.writerows(outputData)
        writeFile.close()
        return True
    return None


def modifyDataToOutput(data):
    result = data
    numRow = len(result)
    for i in range(0, numRow):
        for j in range(0, len(result[i])):
            if type(result[i][j]) != str:
                result[i][j] = repr(result[i][j])
    return result


def normalizationByWidth(data, fieldName, numBox=1):
    field = Attribute(fieldName, [])
    indexField = data[0].index(fieldName)
    for i in range(1, len(data)):
        field.appendData(data[i][indexField])
    floatField = field.convertDataToFloat()
    rangeBox = rangeValid(floatField)/numBox
    flag = []
    start = minValid(floatField)
    end = maxValid(floatField)
    lenField = len(floatField)
    while(start < end):
        for i in range(0, lenField):
            if i not in flag:
                if floatField[i] != '':
                    if floatField[i] >= start:
                        if floatField[i] < (start+rangeBox):
                            floatField[i] = '[' + \
                                str(start)+','+str(start+rangeBox)+')'
                            flag.append(i)
                        elif (start+rangeBox) == end:
                            floatField[i] = '[' + \
                                str(start)+','+str(start+rangeBox)+']'
                            flag.append(i)

                else:
                    flag.append(i)
        start += rangeBox
    field.clear()
    del field
    return Attribute(fieldName, floatField)


def sortField(data):
    if data:
        field = []
        for i in data:
            if i != '':
                field.append(i)
        for i in range(0, len(field)-1):
            if field[i] != '':
                for j in range(i, len(field)):
                    if field[j] != '':
                        if field[j] < field[i]:
                            temp = field[i]
                            field[i] = field[j]
                            field[j] = temp
        return field
    return None


def normalizationByDepth(data, fieldName, numDepth=1):
    field = Attribute(fieldName, [])
    indexField = data[0].index(fieldName)
    for i in range(1, len(data)):
        field.appendData(data[i][indexField])
    floatField = field.convertDataToFloat()
    sortFloat = sortField(floatField)
    flag = []
    i = 0
    k = 0
    remain = len(sortFloat) % numDepth
    start = sortFloat[i]
    end = sortFloat[i+numDepth-1]
    while i < len(sortFloat):
        if k == numDepth:
            k = 0
            if i+numDepth < len(sortFloat):
                start = sortFloat[i]
                end = sortFloat[i+numDepth-1]
            else:
                start = sortFloat[i]
                end = sortFloat[i+remain-1]
        indexItem = floatField.index(sortFloat[i])
        floatField[indexItem] = '['+str(start)+','+str(end)+']'
        k += 1
        i += 1
    field.clear()
    del field
    return Attribute(fieldName, floatField)


def readFieldInFile(fileInput, fieldName):
    with open(fileInput, 'r') as readFile:
        csv_reader = csv.DictReader(readFile)
        result = Attribute(fieldName, [])
        for row in csv_reader:
            result.appendData(row[fieldName])
    readFile.close()
    return result


def readAllInFile(fileInput):
    with open(fileInput, 'r') as readFile:
        csv_reader = csv.reader(readFile)
        result = []
        for row in csv_reader:
            result.append(row)
    readFile.close()
    return result


def deleteMissingValue(data, fieldName):
    result = data
    indexField = result[0].index(fieldName)
    i = 1
    lenResult = len(result)
    while i < lenResult:
        if result[i][indexField] == '':
            result.pop(i)
            lenResult -= 1
        else:
            i += 1
    return result


def insertMissingValue(data, fieldName):
    result = data
    indexField = result[0].index(fieldName)
    attrData = Attribute(fieldName, [])
    for i in range(1, len(data)):
        attrData.appendData(data[i][indexField])
    meanData = mean(attrData.convertDataToFloat())
    if meanData:
        for j in result:
            if j[indexField] == '':
                j[indexField] = meanData
    else:
        freq = frequence(attrData.data)
        for j in result:
            if j[indexField] == '':
                j[indexField] = freq
    attrData.clear()
    del attrData
    return result


def frequence(data):
    freq = [[], []]
    for j in data:
        if j != '':
            if j in freq[0]:
                indexVal = freq[0].index(j)
                if indexVal:
                    freq[1][indexVal] += 1
            else:
                freq[0].append(j)
                freq[1].append(0)
    maxFreq = max(freq[1])
    return freq[0][freq[1].index(maxFreq)]


def minMaxNorm(data, new_range=[0, 1]):  # hàm chuẩn hóa min max
    """Min-Max normalization fuction
         Parameters:
             data : a list values of an numeric attribute 𝐴 that need Min-Max normalization
             new_range: [New_Min,New_Max]  default value is [0,1] if nothing value passed
       Return: An list hold all values that are normalized"""  # day la phan mo ta ham

    min_num = minValid(data)
    max_num = maxValid(data)
    result = []  # mang chua kq tính từng dòng dữ liệu
    for i in data:
        if i != '':
            # cong thuc tinh trong slide
            vi = ((i-min_num)/(max_num-min_num)) * \
                (new_range[1]-new_range[0])+new_range[1]
            result.append(vi)
        else:
            result.append(i)
    return result


def zScoreNorm(data):  # hàm chuẩn hóa Z-scores
    """Z-score normalization fuction
         Parameters:  data : a list values of an numeric attribute 𝐴 that need Z-score normalization
       Return an list hold all values that are normalized"""

    result = []
    d_mean = mean(data)
    d_stddev = stddev(data)  # độ lệch chuẩn
    for i in data:
        if i!='':
         vi = (i-d_mean)/d_stddev
         result.append(vi)
        else:
            result.append(i)
    return result

def mean(data):  # hàm tính trung bình
    "Return the sample arithmetic mean of data"
    if data:
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        sumValid = 0
        lenValid = 0
        for i in data:
            if type(i) == float or type(i) == int or type(i) == complex:
                sumValid += i
                lenValid += 1
        if lenValid > 0:
            return sumValid/lenValid
    return None


def variance(data):  # hàm tính phương sai
    "Return variance of sequence data"
    d_mean = mean(data)
    d_sum = 0
    lenValid=0
    for i in data:
        if i!='':
          lenValid+=1
          d_sum = d_sum + (i-d_mean)**2
    return d_sum/float(lenValid)


def stddev(data):
    "Return standard deviation of sequence data."
    return (variance(data))**0.5


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="input a name of a file csv to read")
parser.add_argument(
    '-o', '--output', help="input a name of a file csv to write")
parser.add_argument('-n', '--nameList',
                    help="input a task what do you want to do with the file", type=str)
parser.add_argument(
    '-t', '--task', help="input a task what do you want to do with the file \n  list of task [min-max,z-core,normWidth,normDepth,remove,insert]")
parser.add_argument(
    '-m', '--min', help="input min of a range to min-max normalization if --task min-max", type=int)
parser.add_argument(
    '-M', '--max', help="input Max of a range to min-max normalization if --task min-max", type=int)
parser.add_argument(
    '-w', '--width', help="input depth to normalization if --task normWidth", type=int)
parser.add_argument(
    '-d', '--depth', help="input depth to normalization if --task normDepth", type=int)
args = parser.parse_args()

if args.nameList:
    nameList = args.nameList.strip()
    for i in nameList:
        if i in '{}[]':
            nameList = nameList.replace(i, '')
    nameList = nameList.split(',')
if args.input and args.output:
    if args.task == 'min-max':        
        attr = readFieldInFile(args.input, nameList[0])
        data = attr.convertDataToFloat()
        minmax_attr = minMaxNorm(
            attr.convertDataToFloat(), [args.min, args.max])
        result = [[nameList[0]]]
        for i in minmax_attr:
            result.append([i])
        lenNameList = len(nameList)
        i = 1
        while(i < lenNameList):
            attr = readFieldInFile(args.input, nameList[i])
            minmax_attr = minMaxNorm(
                attr.convertDataToFloat(), [args.min, args.max])
            result[0].append(nameList[i])
            j = 1
            for k in minmax_attr:
                result[j].append(k)
                j += 1
            i += 1
        writeFieldInFile(args.output,modifyDataToOutput(result))
        attr.clear()
        del attr
    elif args.task=='z-score':
        attr = readFieldInFile(args.input, nameList[0])
        data = attr.convertDataToFloat()
        zscore_attr = zScoreNorm(attr.convertDataToFloat())
        result = [[nameList[0]]]
        for i in zscore_attr:
            result.append([i])
        lenNameList = len(nameList)
        i = 1
        while(i < lenNameList):
            attr = readFieldInFile(args.input, nameList[i])
            zscore_attr = zScoreNorm(attr.convertDataToFloat())
            result[0].append(nameList[i])
            j = 1
            for k in zscore_attr:
                result[j].append(k)
                j += 1
            i += 1
        writeFieldInFile(args.output,modifyDataToOutput(result))
        attr.clear()
        del attr
    elif args.task=='normWidth':
        data = readAllInFile(args.input)
        norm_width=normalizationByWidth(data,nameList[0],args.width)        
        result = norm_width.convertToOutput()        
        lenNameList = len(nameList)
        i = 1
        while(i < lenNameList):
            norm_width=normalizationByWidth(data,nameList[i],args.width) 
            result[0].append(norm_width.name)
            j = 1
            for k in norm_width.data:
                result[j].append(k)
                j += 1
            i += 1
        writeFieldInFile(args.output,modifyDataToOutput(result))
        norm_width.clear()
        del norm_width
    elif args.task=='normDepth':
        data = readAllInFile(args.input)
        norm_depth=normalizationByDepth(data,nameList[0],args.depth)        
        result = norm_depth.convertToOutput()        
        lenNameList = len(nameList)
        i = 1
        while(i < lenNameList):
            norm_depth=normalizationByDepth(data,nameList[i],args.depth) 
            result[0].append(norm_depth.name)
            j = 1
            for k in norm_depth.data:
                result[j].append(k)
                j += 1
            i += 1
        writeFieldInFile(args.output,modifyDataToOutput(result))
        norm_depth.clear()
        del norm_depth
    elif args.task=='remove':
        data = readAllInFile(args.input)
        for i in nameList:
            data=deleteMissingValue(data,i)
        writeFieldInFile(args.output,modifyDataToOutput(data))
    elif args.task=='insert':
        data = readAllInFile(args.input)
        for i in nameList:
            data=insertMissingValue(data,i)
        writeFieldInFile(args.output,modifyDataToOutput(data))   

exit()

