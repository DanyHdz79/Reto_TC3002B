# Writing to an excel sheet using Python 
import xlwt
import os
import re


def get_word_percentage(f, f2, word):
    f = f.count(word)
    f2 = f2.count(word)
    x = max(f, f2)
    y = min(f, f2)
    if x == 0:
        return 0
    return (y/x)

# Workbook is created 
workbook = xlwt.Workbook()

# add_sheet is used to create sheet. 
sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

path = "./../c_output"
dir_list = os.listdir(path)
count = 1

label = open("./../SOCO14-c.qrel", "r")
lines = label.readlines()
 
sheet.write(0, 0, 'File Names')
sheet.write(0, 1, 'Per_Functions')
sheet.write(0, 2, 'Per_Loops')
sheet.write(0, 3, 'Per_Conditionals')
sheet.write(0, 4, 'Per_Arithmetic_Operations')
sheet.write(0, 5, 'Per_int_Declarations')
sheet.write(0, 6, 'Per_float_Declarations')
sheet.write(0, 7, 'Per_char_Declarations')
sheet.write(0, 8, 'label')
 
for file in dir_list:
    f = open(path+"/"+file, "r").read()
    f = re.sub(r"\s+", " ", f)
    for file2 in dir_list:
        f2 = open(path+"/"+file2, "r").read()
        f2 = re.sub(r"\s+", " ", f2)

        if file != file2:
            sheet.write(dir_list.index(file) + count, 0, file + " " + file2)

            per_functions = get_word_percentage(f, f2, "function")
            sheet.write(dir_list.index(file) + count, 1, per_functions)

            per_loops = get_word_percentage(f, f2, "loop")
            sheet.write(dir_list.index(file) + count, 2, per_loops)
            
            per_conditionals = get_word_percentage(f,f2,"conditional")
            sheet.write(dir_list.index(file) + count, 3, per_conditionals)

            per_arithmetic_operations = get_word_percentage(f,f2,"arithmetic_operation")
            sheet.write(dir_list.index(file) + count, 4, per_arithmetic_operations)
            
            per_int_declarations = get_word_percentage(f,f2,"int")
            sheet.write(dir_list.index(file) + count, 5, per_int_declarations)

            per_float_declarations = get_word_percentage(f,f2,"float")
            sheet.write(dir_list.index(file) + count, 6, per_float_declarations)
            
            per_char_declarations = get_word_percentage(f,f2,"char")
            sheet.write(dir_list.index(file) + count, 7, per_char_declarations)

            for line in lines:
                if file in line and file2 in line:
                    sheet.write(dir_list.index(file) + count, 8, 1)
                    break
                else:
                    sheet.write(dir_list.index(file) + count, 8, 0)
            count += 1
    count-= 1

    
workbook.save('code_plagiarism.xls')
