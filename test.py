import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score


df = pd.read_csv("dog_classification_vs_circumstances_test.csv")

accuracy = accuracy_score(y_pred=df.DogClassification, y_true=df.TrueLabel) #0.7019230769230769
recall = recall_score(y_pred=df.DogClassification, y_true=df.TrueLabel,average=None, labels=['Family Dog', 'Not Family', 'Stray Dog', 'Unknown']) #[0.88888889, 0.62857143, 0.75      , 0.3125    ]
precision = precision_score(y_true=df.TrueLabel, y_pred=df.DogClassification, average=None, labels=['Family Dog', 'Not Family', 'Stray Dog', 'Unknown']) #[0.8       , 0.57894737, 0.75      , 0.625     ]
f1score  = f1_score(y_true=df.TrueLabel, y_pred=df.DogClassification, average=None, labels=['Family Dog', 'Not Family', 'Stray Dog', 'Unknown']) #[0.84210526, 0.60273973, 0.75      , 0.41666667]