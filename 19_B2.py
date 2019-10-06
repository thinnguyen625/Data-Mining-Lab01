import sys
import csv
import pandas as pd 

def process_file_text():
    with open("countries.txt", "r",encoding="utf8") as fi:
        with open("fileConvert.csv", 'w',encoding="utf8",newline='') as writeFile:
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

def readAllInFile(fileInput):
    with open(fileInput,"r",encoding="utf8") as readFile:
        csv_reader = csv.reader(readFile)
        result = []
        for row in csv_reader:
            result.append(row)
    readFile.close()
    return result

def delete_empty_set(data): #xóa tập rỗng
    result = data
    i=0
    while i<len(result):
        for j in range(1,len(result[i])):
            if result[i][j]!='':
                i+=1
                break
            if j==len(result[i])-1:
                del result[i]
    return result

def convert_area(data): #chuyển diện tích về km = mi / 0.38610
    result = data
    i=0
    while i<len(result):
        j = len(result[i])- 1
        str_area = result[i][j]
        if str_area == '':
           i+=1
           continue
        x = 'mi' in str_area
        y = ' ' in str_area
        z = ',' in str_area
        if x == True and y == False:
            str_area = str_area.split('m')
            num=float(str_area[0])
            num = num / float(0.38610)
            result[i][j]=str(num)+"km"
        if x== True and y==True and z==False:
            str_area = str_area.split('m')
            temp=str_area[0].split(' ')
            num=float(temp[1])
            num = num / float(0.38610)
            result[i][j]=str(num)+"km"
        if x==True and y==True and z==True:
            str_area = str_area.split('m')
            temp=str_area[0].split(' ')
            temp_sothuc=temp[1].split(',')

            num_truoc=float(temp_sothuc[0])
            num_sau=float(temp_sothuc[1])
            num=num_truoc+num_sau*(0.1)
            num = num / float(0.38610)
            result[i][j]=str(num)+"km"
        i+=1
    return result
        
def delete_duplicate_set(data): #xóa tập trùng nhau
    result = data
    i=0
    while i<len(result):
        for j in range(1,8):
            if result[i][j]!=result[i-1][j]:
                i+=1
                break
            if j==len(result[i])-1:
                del result[i]
    return result

def delete_no_area_set(data): #xóa tập bị thiếu diện tích
    result = data
    i=0
    while i<len(result):
        j = len(result[i])- 1
        if result[i][j]!='':
            i+=1
            continue
        else: 
            del result[i]
    return result
        
def writeFieldInFile(fileOutput, data):
    if data:
        with open(fileOutput, mode='w', newline='') as writeFile:
            csv_writer = csv.writer(writeFile)
            csv_writer.writerows(data)
        writeFile.close()
        return True
    return None

def main():
    process_file_text()
    file_in = "fileConvert.csv"
    file_out = "19_B2.csv"

    data = readAllInFile(file_in)
    data_1 = delete_empty_set(data)
    data_2 = delete_no_area_set(data_1)
    data_3 = delete_duplicate_set(data_2)
    data_4 = convert_area(data_3)

    writeFieldInFile(file_out, data_4)
    data.clear()

if __name__ == '__main__':
    main()


