import preprocess
from joblib import load
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


columns_to_drop = ["File Name 1", "File Name 2", "Per_float_Declarations"]
model = load('./neuronal_net.joblib')
print("carga load")


with open('./../SOCO14-c_copy.qrel','r') as f:
    for line in f:
        files = line.split()
        file1 = files[0]
        file2 = files[1]

        data = preprocess.tokenize(file1, file2)

        data = data.drop(columns_to_drop, axis = 1)

        per_plagiarism = model.predict(data)

        print(f"Plagio entre {file1} y {file2}: {per_plagiarism}")

