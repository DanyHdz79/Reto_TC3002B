import preprocess
from joblib import load
import pandas as pd

file1 = input("Name of the first file: ")
file2 = input("Name of the second file: ")

preprocess.tokenize(file1, file2)

data = pd.read_excel("./new_input.xls")
columns_to_drop = ["File Name 1", "File Name 2", "Per_float_Declarations"]
data = data.drop(columns_to_drop, axis = 1)

model = load('random_forest.joblib')

per_plagiarism = model.predict(data)

print(per_plagiarism)

