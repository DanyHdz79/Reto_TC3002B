# Writing to an excel sheet using Python 
import xlwt
import os
import re

# Workbook is created 
workbook = xlwt.Workbook()

# add_sheet is used to create sheet. 
sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

path = "./../c"
dir_list = os.listdir(path)
count = 1

label = open("./../SOCO14-c.qrel", "r")
lines = label.readlines()
 
sheet.write(0, 0, 'File Name 1')
sheet.write(0, 1, 'Code 1')
sheet.write(0, 2, 'File Name 2')
sheet.write(0, 3, 'Code 2')
sheet.write(0, 4, 'label')
 
for file in dir_list:
    f = open(path+"/"+file, "r").read()
    f = re.sub(r"\s+", " ", f)
    for file2 in dir_list:
        f2 = open(path+"/"+file2, "r").read()
        f2 = re.sub(r"\s+", " ", f2)

        if file != file2:
            sheet.write(dir_list.index(file) + count, 0, file)
            sheet.write(dir_list.index(file) + count, 1, f)
            sheet.write(dir_list.index(file) + count, 2, file2)
            sheet.write(dir_list.index(file) + count, 3, f2)

            for line in lines:
                if file in line and file2 in line:
                    sheet.write(dir_list.index(file) + count, 4, 1)
                    break
                else:
                    sheet.write(dir_list.index(file) + count, 4, 0)
            count += 1
    count-= 1

    
workbook.save('code_plagiarism.xls')
