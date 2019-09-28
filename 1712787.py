import csv

def main_cau_e():
    inputfile = "original.csv"
    field_input=[]   
    with open(inputfile, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames
        input_filedname="passenger_numbers"
        data=[]
        for row in csv_reader:
                data.append((row[input_filedname]))
        result_del = delete_missing_value(data)
        length_data=len(result_del)
        for i in range(0,length_data):
            print(f'{result_del[i]}')
        # result_insert = insert_missing_value(data)
        # for i in range(0,len(result_insert)):
        #     print(f'{result_insert[i]}')
       

def delete_missing_value(data): #Xóa các mẫu dữ liệu thiếu giá trị
    result = []
    result = data
    result = list(filter(None, result))
    return result
def insert_missing_value(data): #Thêm các mẫu dữ liệu thiếu giá trị
    result = []
    result = data
    # n = 0 #so luong so khac null
    # s = 0
    # for i in result:
    #     if i.isdigit()==True:
    #         n+=1
    #         s+=int(i)
    # mean=s/float(n)
    # for i in result:
    #     if i.isdigit()==False:
    #         i = mean
    return result
    
        

if __name__ == '__main__':
    main_cau_e()
    exit()
