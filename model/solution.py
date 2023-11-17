import preprocess
from joblib import load
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

file1 = input("Name of the first file: ")
file2 = input("Name of the second file: ")

data = preprocess.tokenize(file1, file2)

columns_to_drop = ["File Name 1", "File Name 2", "Per_float_Declarations"]
data = data.drop(columns_to_drop, axis = 1)

print(data)
model = load('./neuronal_net.joblib')
print("carga load")
per_plagiarism = model.predict(data)

print(per_plagiarism)

