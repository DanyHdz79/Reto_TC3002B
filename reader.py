import os

file = 0

for i in range(1, 79):
    if file < 10:
        os.system(f"lexical_analyzer/lexer < c/00{file}.c > c_output/00{file}.txt")
    else:
        os.system(f"lexical_analyzer/lexer < c/0{file}.c > c_output/0{file}.txt")
    file+=1