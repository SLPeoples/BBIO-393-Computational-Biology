"""
breastCancer.py
Random Forest Classification
Predicting Malignancy of Breast Cancer data
2: Benign, 4: Malignant
"""

# Importing the libraries
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('breastCancer.csv')
X = dataset.iloc[:, 1:10].values
y = dataset.iloc[:, 10].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy')
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)