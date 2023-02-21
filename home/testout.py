import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split as split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump, load

save_path = "saved_model/"
model_name = "model"

import os

data = pd.read_csv(r'Maternal Health Risk Data Set.csv')

print(data.head())

print(f"There are {data.duplicated().sum()} duplicates data")
data.loc[data.duplicated(keep=False)].sort_values(by=data.columns.to_list())

data_proc = data.drop(data.index[data.HeartRate == 7])

data_proc = data_proc.drop(["HeartRate"], axis=1)

# Original Dataset
X = data.drop("RiskLevel", axis=1)
y = data.RiskLevel
x_train, x_test, y_train, y_test = split(X, y, test_size=0.2, random_state=1)

# Processed Dataset
X_proc = data_proc.drop("RiskLevel", axis=1)
y_proc = data_proc.RiskLevel
x_train_proc, x_test_proc, y_train_proc, y_test_proc = split(X_proc, y_proc, test_size=0.2, random_state=1)

# Using original dataset
rf = RandomForestClassifier(random_state=100)
rf.fit(x_train, y_train)
y_pred = rf.predict(x_test)
print(f"Original Dataset Accuracy: {accuracy_score(y_test, y_pred)}")

# Using processed dataset
rf2 = RandomForestClassifier(random_state=100)

print(x_test_proc.iloc[[35]])
rf2.fit(x_train_proc, y_train_proc)
dump(rf2, str(save_path + model_name + ".joblib"))
y_pred = rf2.predict(x_test_proc)
predlen = x_test_proc.iloc[35].to_numpy().reshape(1, -1)
print(predlen)
print(y_test_proc.iloc[35])
testpred = rf2.predict(predlen)
print(testpred)
print(f"Processed Dataset Accuracy: {accuracy_score(y_test_proc, y_pred)}")