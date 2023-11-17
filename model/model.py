import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import tensorflow as tf
from tensorflow.keras import layers
import keras
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_excel("./code_plagiarism.xls")

non_zero_cells_per_column = data.astype(bool).sum(axis=0)
percentages_non_zero_cells_per_column = (non_zero_cells_per_column * 100) / (data.shape[0])

# Obtaining the columns that have more than 90% of null values
columns_to_drop = percentages_non_zero_cells_per_column < 10
columns_to_drop = columns_to_drop[columns_to_drop]
columns_to_drop = columns_to_drop.index
columns_to_drop = columns_to_drop.drop("label")

clean_data = data.drop(columns_to_drop, axis = 1)

X = clean_data.drop(["File Name 1", "File Name 2", "label"], axis = 1)
y = clean_data["label"]

over = SMOTE(sampling_strategy=0.07)
under = RandomUnderSampler(sampling_strategy=0.35)

steps = [('o', over), ('u', under)]
pipeline = Pipeline(steps=steps)

X, y = pipeline.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

assert X_train.shape[0] == y_train.shape[0]
input_dim = X_train.shape[1]
outuput_dim = 1

model = keras.models.Sequential([
    keras.layers.Dense(256, activation=tf.nn.relu, input_shape=(X_train.shape[1],)),
    keras.layers.Dense(256, activation=tf.nn.relu),
    keras.layers.Dense(256, activation=tf.nn.relu),
    keras.layers.Dense(outuput_dim, activation=tf.nn.sigmoid)
])    

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

print(model.summary())

history = model.fit(X_train, y_train, workers=4, epochs=50, verbose=2)
print(history)

# Convertimos el historico a dataframe (formato de pandas)
df = pd.DataFrame(history.history)

# creamos un espacio para pintar nuestros graficos
f = plt.figure(figsize=(16, 5))

rows = 1
cols = 2

# Gráfico a la izquierda, vemos el accuracy de nuestro conjunto de entrada vs conjunto de validación.
ax = f.add_subplot(rows, cols, 1)
sns.lineplot(data=df["accuracy"].iloc[3:-1])


# Gráfico a la derecha, vemos el loss de nuestro conjunto de entrada vs conjunto de validación.
ax = f.add_subplot(rows, cols, 2)
sns.lineplot(data=df["loss"].iloc[3:-1]);

dump(model, './neuronal_net.joblib')