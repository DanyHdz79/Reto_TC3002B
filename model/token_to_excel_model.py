# Writing to an excel sheet using Python 
import xlwt
import os
import re
from math import sqrt, pow, exp
import spacy


def tokenize():
    file = 0
    for i in range(1, 79):
        if file < 10:
            os.system(f"./../lexical_analyzer/lexer < ./../data/c/00{file}.c > ./../data/c_output/00{file}.c")
        else:
            os.system(f"./../lexical_analyzer/lexer < ./../data/c/0{file}.c > ./../data/c_output/0{file}.c")
        file+=1

def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

def squared_sum(x):
  """ return 3 rounded square rooted value """
 
  return round(sqrt(sum([a*a for a in x])),3)
 
def euclidean_distance(x,y):
  """ return euclidean distance between two lists """
 
  return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

def distance_to_similarity(distance):
  return 1/exp(distance)
  

def get_word_percentage(f, f2, word):
    f = f.count(word)
    f2 = f2.count(word)
    x = max(f, f2)
    y = min(f, f2)
    if x == 0:
        return 0
    return (y/x)


def get_declaration_percentage(f, f2, word):
    word_counter_f = 0
    f = f.split()
    for i in range(0, len(f)):
        if f[i] == word:
            word_counter_f += 1
            i += 1
            while(f[i] != 'semicolon'):
                i += 1
                word_counter_f += 1
    
    word_counter_f2 = 0
    f2 = f2.split()
    for i in range(0, len(f2)):
        if f2[i] == word:
            word_counter_f2 += 1
            i += 1
            while(f2[i] != 'semicolon'):
                i += 1
                word_counter_f2 += 1

    x = max(word_counter_f, word_counter_f2)
    y = min(word_counter_f, word_counter_f2)
    if x == 0:
        return 0
    return (y/x)

# Workbook is created 
workbook = xlwt.Workbook()

# add_sheet is used to create sheet. 
sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

path = "./../data/c_output"
path_o = "./../data/c"

dir_list = os.listdir(path)
count = 1

label = open("./../SOCO14-c.qrel", "r")
lines = label.readlines()
 
sheet.write(0, 0, 'File Name 1')
sheet.write(0, 1, 'File Name 2')
sheet.write(0, 2, 'Per_Functions')
sheet.write(0, 3, 'Per_Loops')
sheet.write(0, 4, 'Per_Conditionals')
sheet.write(0, 5, 'Per_Arithmetic_Operations')
sheet.write(0, 6, 'Per_int_Declarations')
sheet.write(0, 7, 'Per_float_Declarations')
sheet.write(0, 8, 'Per_char_Declarations')
sheet.write(0, 9, 'Jaccard_Metric')
sheet.write(0, 10, 'Euclidean_Distance')
sheet.write(0, 11, 'label')

nlp = spacy.load("en_core_web_sm")

files_names = []
 
for file in dir_list:
    f = open(path+"/"+file, "r").read()
    f = re.sub(r"\s+", " ", f)

    f_o = open(path_o+"/"+file, "r").read()
    f_o = re.sub(r"\s+", " ", f)
    for file2 in dir_list:
        print(file, file2)
        f2 = open(path+"/"+file2, "r").read()
        f2 = re.sub(r"\s+", " ", f2)

        f2_o = open(path_o+"/"+file2, "r").read()
        f2_o = re.sub(r"\s+", " ", f2)

        if file != file2 and ((file+file2 not in files_names) and (file2+file not in files_names)):
            sheet.write(dir_list.index(file) + count, 0, file)
            sheet.write(dir_list.index(file) + count, 1, file2)

            per_functions = get_word_percentage(f, f2, "function")
            sheet.write(dir_list.index(file) + count, 2, per_functions)

            per_loops = get_word_percentage(f, f2, "loop")
            sheet.write(dir_list.index(file) + count, 3, per_loops)
            
            per_conditionals = get_word_percentage(f,f2,"conditional")
            sheet.write(dir_list.index(file) + count, 4, per_conditionals)

            per_arithmetic_operations = get_word_percentage(f,f2,"arithmetic_operation")
            sheet.write(dir_list.index(file) + count, 5, per_arithmetic_operations)
            
            per_int_declarations = get_declaration_percentage(f,f2,"int_variable")
            sheet.write(dir_list.index(file) + count, 6, per_int_declarations)

            per_float_declarations = get_declaration_percentage(f,f2,"float_variable")
            sheet.write(dir_list.index(file) + count, 7, per_float_declarations)
            
            per_char_declarations = get_declaration_percentage(f,f2,"char_variable")
            sheet.write(dir_list.index(file) + count, 8, per_char_declarations)

            sentences = [f_o, f2_o]
            sentences_1 = [sent.lower().split(" ") for sent in sentences]
            jaccard_metric = jaccard_similarity(sentences_1[0], sentences_1[1])
            sheet.write(dir_list.index(file) + count, 9, jaccard_metric)

            embeddings = [nlp(sentence).vector for sentence in sentences]
            distance = euclidean_distance(embeddings[0], embeddings[1])
            euclidean_metric = distance_to_similarity(distance) 
            sheet.write(dir_list.index(file) + count, 10, euclidean_metric)

            for line in lines:
                if file in line and file2 in line:
                    sheet.write(dir_list.index(file) + count, 11, 1)
                    break
                else:
                    sheet.write(dir_list.index(file) + count, 11, 0)
            
            files_names.append(file+file2)

            count += 1
    count-= 1

    
workbook.save('code_plagiarism.xls')
