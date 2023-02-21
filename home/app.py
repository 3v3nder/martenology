import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import keras 
from keras.models import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load

save_path = "saved_model/"
model_name = "model"

data = pd.read_csv(r'Maternal Health Risk Data Set.csv')

data.head()

data.shape

sns.pairplot(data, hue='RiskLevel')

data.isnull().sum()

df = pd.get_dummies(data)
df.head()

df.describe()

X = df.iloc[:, 0:-1]
Y = df.iloc[:, -1]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
print('Shape of X_train:', X_train.shape)
print('Shape of y_train:', y_train.shape)
print("Shape of X_test:", X_test.shape)
print("Shape of y_test:", y_test.shape)

classifier = Sequential()

classifier.add(Dense(4, kernel_initializer='uniform', activation='relu', input_dim=8))
classifier.add(Dense(4, kernel_initializer='uniform', activation='relu'))
classifier.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))


classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=["Accuracy"])

classifier.fit(X_train, y_train, batch_size=20, epochs=100)

y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

cm

sns.heatmap(cm,annot=True)
plt.savefig('h.png')

model = RandomForestClassifier()
model.fit(X_train, y_train)
dump(model, str(save_path + model_name + ".joblib"))
model.score(X_test, y_test)

patient1 = [00.1, 2.000, 00.5542, 000.4235, 0.325, 0.856, 0.6985, 00.2568]

patient1 = np.array([patient1])
patient1


Y_pred = classifier.predict(patient1)
print(Y_pred)

if Y_pred == 1:
  print('Patients has High Risk')
elif Y_pred == 0:
  print('Patients has Low Risk')
else:
  print('Patients has Mid Risk')