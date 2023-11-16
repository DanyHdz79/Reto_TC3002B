import os
import xlwt
import re
from math import sqrt, pow, exp
import spacy

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
                
            

def tokenize(file1, file2):
    # Tokenize the files
    os.system(f"./../lexical_analyzer/lexer < ./../data/c/{file1} > ./../data/examples_c_output/{file1}")
    os.system(f"./../lexical_analyzer/lexer < ./../data/c/{file2} > ./../data/examples_c_output/{file2}")



    # Workbook is created 
    workbook = xlwt.Workbook()

    # add_sheet is used to create sheet. 
    sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)


    path = "./../data/examples_c_output"
    path_o = "./../data/c"

    nlp = spacy.load("en_core_web_sm")

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

    f1 = open(path + "/" + file1, "r").read()
    f1 = re.sub(r"\s+", " ", f1)
    f1_o = open(path_o+"/"+file1, "r").read()
    f1_o = re.sub(r"\s+", " ", f1)

    f2 = open(path + "/" + file2, "r").read()
    f2 = re.sub(r"\s+", " ", f2)
    f2_o = open(path_o+"/"+file2, "r").read()
    f2_o = re.sub(r"\s+", " ", f2)

    sheet.write(1, 0, file1)
    sheet.write(1, 1,  file2)


    per_functions = get_word_percentage(f1, f2, "function")
    sheet.write(1, 2, per_functions)

    per_loops = get_word_percentage(f1, f2, "loop")
    sheet.write(1, 3, per_loops)
                
    per_conditionals = get_word_percentage(f1,f2,"conditional")
    sheet.write(1, 4, per_conditionals)

    per_arithmetic_operations = get_word_percentage(f1,f2,"arithmetic_operation")
    sheet.write(1, 5, per_arithmetic_operations)
            
    per_int_declarations = get_declaration_percentage(f1,f2,"int_variable")
    sheet.write(1, 6, per_int_declarations)

    per_float_declarations = get_declaration_percentage(f1,f2,"float_variable")
    sheet.write(1, 7, per_float_declarations)
            
    per_char_declarations = get_declaration_percentage(f1,f2,"char_variable")
    sheet.write(1, 8, per_char_declarations)

    sentences = [f1_o, f2_o]
    sentences_1 = [sent.lower().split(" ") for sent in sentences]
    jaccard_metric = jaccard_similarity(sentences_1[0], sentences_1[1])
    sheet.write(1, 9, jaccard_metric)

    embeddings = [nlp(sentence).vector for sentence in sentences]
    distance = euclidean_distance(embeddings[0], embeddings[1])
    euclidean_metric = distance_to_similarity(distance) 
    sheet.write(1, 10, euclidean_metric)



    workbook.save('new_input.xls')
