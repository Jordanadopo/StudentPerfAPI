"""

The goal of this experiment is to develop a model that will predict (to a certain level of acceptable accuracy) whether a student will pass or fail a mathematics course over a year (two semesters).
The features will consist of all given features within the dataset excluding the GX factors that represent semester grades. G3 will be the target feature.

"""

""" Import helper libraries """
import numpy as np
import pandas as pd


""" Import ML helpers """
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score

from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import LinearSVC # Support Vector Machine Classifier model
import os
from api.settings import BASE_DIR

class Predictor:
    base_dir = os.path.join(BASE_DIR, 'passpredictor/models')

    #load dataset of student portuguese scores
    d1 = pd.read_csv(os.path.join(base_dir,'dataset/student-por.csv'), sep=';')
    d2 = pd.read_csv(os.path.join(base_dir,'dataset/student-mat.csv'), sep=';')
    class_le = LabelEncoder()

    def __init__(self):
        """ Read data file as DataFrame """
        

        self.df = pd.concat([self.d1, self.d2])

        # For each feature, encode to categorical values
        for column in self.df[["school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", "reason", "guardian", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]].columns:
            self.df[column] = self.class_le.fit_transform(self.df[column].values)

        self.get_dummies(self.df)
        self.train_and_score()

    def split_data(self, X, Y):
        """ Split Data into Training and Testing Sets """
        return train_test_split(X, Y, test_size=0.2, random_state=17)

    def confuse(self, y_true, y_pred):
        """ Confusion Matrix """
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
        # print("\nConfusion Matrix: \n", cm)
        self.fpr(cm)
        self.ffr(cm)

    def fpr(self, confusion_matrix):
        """ False Pass Rate """
        fp = confusion_matrix[0][1]
        tf = confusion_matrix[0][0]
        rate = float(fp) / (fp + tf)
        print("False Pass Rate: ", rate)

    def ffr(self,confusion_matrix):
        """ False Fail Rate """
        ff = confusion_matrix[1][0]
        tp = confusion_matrix[1][1]
        rate = float(ff) / (ff + tp)
        print("False Fail Rate: ", rate)

        return rate

    def train_and_score(self):
        # Target values are G3
        y = self.df.pop("G3")

        # Feature set is remaining features
        X = self.df
        """ Train Model and Print Score """
        X_train, X_test, y_train, y_test = self.split_data(X, y)

        self.clf = Pipeline([
            ('reduce_dim', SelectKBest(chi2, k=2)),
            ('train', LinearSVC(C=100))
        ])

        scores = cross_val_score(self.clf, X_train, y_train, cv=5, n_jobs=2)
        print("Mean Model Accuracy:", np.array(scores).mean())

        self.clf.fit(X_train, y_train)

        self.confuse(y_test, self.clf.predict(X_test))
        print()

    def get_dummies(self, data):
        
        # Encode G1, G2, G3 as pass or fail binary values
        for i, row in data.iterrows():
            if row["G1"] >= 10:
                data["G1"][i] = 1
            else:
                data["G1"][i] = 0

            if row["G2"] >= 10:
                data["G2"][i] = 1
            else:
                data["G2"][i] = 0

            if 'G3' in row:
                if row["G3"] >= 10:
                    data["G3"][i] = 1
                else:
                    data["G3"][i] = 0

        

    def fit_transform(self, data):
        for column in self.df[["school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", "reason", "guardian", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]].columns:
            data[column] = self.class_le.fit_transform(data[column].values)

    def predict(self, data):
        data = pd.json_normalize(data)
        self.fit_transform(data)
        self.get_dummies(data)
        return self.clf.predict(data)


# """ Main test Program """
# def main():
#     print("\nStudent Performance Prediction")

#     mod = Predictor()
    

    

#     # # Remove grade report 2
#     # X.drop(["G2"], axis = 1, inplace=True)
#     # print("\n\nModel Accuracy Knowing Only G1 Score")
#     # print("=====================================")
#     # mod.train_and_score(X, y)

#     # # Remove grade report 1
#     # X.drop(["G1"], axis=1, inplace=True)
#     # print("\n\nModel Accuracy Without Knowing Scores")
#     # print("=====================================")
#     # mod.train_and_score(X, y)

#     print(mod.clf)
#     a = {   "school": "MS",
#             "sex": "M",
#             "age": 17,
#             "address": "U",
#             "famsize": "GT3",
#             "Pstatus": "A",
#             "Medu": 3,
#             "Fedu": 0,
#             "Mjob": "services",
#             "Fjob": "services",
#             "reason": "course",
#             "guardian": "mother",
#             "traveltime": 3,
#             "studytime": 3,
#             "failures": "0",
#             "schoolsup": 'yes',
#             "famsup": 'yes',
#             "paid": 'yes',
#             "activities": 'yes',
#             "nursery": 'yes',
#             "higher": 'yes',
#             "internet": 'yes',
#             "romantic": 'yes',
#             "famrel": 3,
#             "freetime": 2,
#             "goout": 2,
#             "Dalc": 1,
#             "Walc": 1,
#             "health": 4,
#             "absences": 0,
#             "G1": 15,
#             "G2": 14
#         }

#     print(mod.predict(a))



# main()