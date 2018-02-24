import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

dataset = pd.read_csv('tickets_train.csv',encoding="cp1252")

corpus = []
for i in range(237):
    #removing anything apart from characters from the review
    detail = re.sub('[^a-zA-Z]', ' ', dataset['Detail'][i])
    #making the review words to lower 
    detail = detail.lower()
    #makinga list out of the review words
    detail = detail.split()
    ps = PorterStemmer()
    #removing the stopwords from review and stemming
    detail = [ps.stem(word) for word in detail if not word in set(stopwords.words('english'))]
    #making the review back to a string
    detail = ' '.join(detail)
    corpus.append(detail)

# Creating the Bag of Words model

cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:,3].values

with open('cv.pkl', 'wb') as f:
    pickle.dump(cv, f)

# Using Naive Bayes classifier

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

#print(X_test)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
y_pred_nb = classifier.predict(X_test)

'''# fitting RandomForest
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)'''

with open('model.pkl', 'wb') as f:
    pickle.dump(classifier, f)

'''y_pred_rf = classifier.predict(X_test)

#print(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred_nb)
print(y_pred_rf)'''