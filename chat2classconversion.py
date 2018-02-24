import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
data = "Desktop not working"

class MLhelper():

    def get_department(self,data):
        with open('cv.pkl', 'rb') as f:
            cv = pickle.load(f)

        detail = re.sub('[^a-zA-Z]', ' ', data)
        detail = detail.lower()
        detail = detail.split()
        ps = PorterStemmer()
        detail = [ps.stem(word) for word in detail if not word in set(stopwords.words('english'))]
        detail = ' '.join(detail)
        corpus = []
        corpus.append(detail)

        X = cv.transform(corpus).toarray()

        with open('model.pkl', 'rb') as f:
            clf = pickle.load(f)

        pred = clf.predict(X)
        print("predcited department: " + str(pred))
        return(str(pred[0]))
