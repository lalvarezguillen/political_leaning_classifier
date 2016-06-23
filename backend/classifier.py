from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from .tools.database_stuff import db
import classifier_config
import os
import datetime


if classifier_config.pickled_classifier: #If we're using a stored classifier
    classif_pipe = joblib.load(classifier_config.pickled_classifier)
else: #If we're creating/using a new classifier
    classif_pipe = trainClassifier()


def trainClassifier():
    """ Trains a classifier with the current dataset """
    classif_pipe = Pipeline([
        ("vect", TfidfVectorizer(analyzer="word", ngram_range=(1,2), stop_words="english", max_df=1.0 )),
        ("clf", MultinomialNB())
    ])
    
    print("Generating training data....")
    training_data = []
    labels = []
    for entry in db.execute("SELECT * from statements"): #(statement, leaning, author)
        training_data.append(entry[0])
        labels.append(entry[1])
    
    print("Training the classifier...")    
    classif_pipe.fit(training_data, labels)
    
    print("Pickling and storing the classifier...")
    storeClassifier(classif_pipe)
    
    return classif_pipe
    
    
def storeClassifier(model):
    """ Stores the trained classifier in hard drive, to make it available for later use """
    if not os.path.isdir("pickled_classifiers"):
        os.makedirs("pickled_classifiers")
        
    joblib.dump(
        model,
        "pickled_classifiers/classifier_{}".format(datetime.date.today())
    )

#TODO: Create some code to benchmark the classifier's precision
#And store the precision info as classifier's metada, for later usage