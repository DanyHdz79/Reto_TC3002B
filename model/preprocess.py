import os
import re
from math import sqrt, pow, exp
import spacy
import pandas as pd

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


    path = "./../data/examples_c_output"
    path_o = "./../data/c"

    nlp = spacy.load("en_core_web_sm")

    f1 = open(path + "/" + file1, "r").read()
    f1 = re.sub(r"\s+", " ", f1)
    f1_o = open(path_o+"/"+file1, "r").read()
    f1_o = re.sub(r"\s+", " ", f1)

    f2 = open(path + "/" + file2, "r").read()
    f2 = re.sub(r"\s+", " ", f2)
    f2_o = open(path_o+"/"+file2, "r").read()
    f2_o = re.sub(r"\s+", " ", f2)

    df = pd.DataFrame(columns=['File Name 1', 'File Name 2', 'Per_Functions', 'Per_Loops','Per_Conditionals','Per_Arithmetic_Operations','Per_int_Declarations','Per_float_Declarations','Per_char_Declarations','Jaccard_Metric','Euclidean_Distance'])


    per_functions = get_word_percentage(f1, f2, "function")

    per_loops = get_word_percentage(f1, f2, "loop")
                
    per_conditionals = get_word_percentage(f1,f2,"conditional")

    per_arithmetic_operations = get_word_percentage(f1,f2,"arithmetic_operation")
            
    per_int_declarations = get_declaration_percentage(f1,f2,"int_variable")

    per_float_declarations = get_declaration_percentage(f1,f2,"float_variable")
            
    per_char_declarations = get_declaration_percentage(f1,f2,"char_variable")

    sentences = [f1_o, f2_o]
    sentences_1 = [sent.lower().split(" ") for sent in sentences]
    jaccard_metric = jaccard_similarity(sentences_1[0], sentences_1[1])

    embeddings = [nlp(sentence).vector for sentence in sentences]
    distance = euclidean_distance(embeddings[0], embeddings[1])
    euclidean_metric = distance_to_similarity(distance) 

    df.loc[0] = [file1, file2, per_functions, per_loops, per_conditionals, per_arithmetic_operations, per_int_declarations, per_float_declarations, per_char_declarations, jaccard_metric, euclidean_metric]


    return df
