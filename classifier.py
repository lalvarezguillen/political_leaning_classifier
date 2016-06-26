from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from tools.database_stuff import db
import classifier_config
import os
import datetime
import random

def generateBalancedDataset():
    right = []
    left = []
    for entry in db.execute("SELECT * from statements"):
        if entry[1] == "right": right.append(entry)
        elif entry[1] == "left": left.append(entry)
        
    if len(right) > len(left): right = right[:len(left)]
    elif len(right) < len(left): left = left[:len(right)]
    
    data = right + left
    random.shuffle(data)

    return (
        [e[0] for e in data],
        [e[1] for e in data]
        )
    
def trainClassifier():
    """ Trains a classifier with the current dataset """
    classif_pipe = Pipeline([
        ("vect", TfidfVectorizer(analyzer="word", ngram_range=(1,3), stop_words="english", max_df=0.7, min_df=5 )),
        ("clf", MultinomialNB())
    ])
    
    print("Generating training and testing data....")
    statements, labels = generateBalancedDataset()
    testing_slice = int(len(statements)*0.02)
    training_statements = statements[testing_slice:]
    testing_statements = statements[:testing_slice]
    training_labels = labels[testing_slice:]
    testing_labels = labels[:testing_slice]
    
    print("Training the classifier...")    
    classif_pipe.fit(training_statements, training_labels)
    
    print("Pickling and storing the classifier...")
    storeClassifier(classif_pipe)
    
    print("The model's accuracy is {}".format(
        classif_pipe.score(testing_statements, testing_labels)
        ))
    
    return classif_pipe
    
    
def storeClassifier(model):
    """ Stores the trained classifier in hard drive, to make it available for later use """
    if not os.path.isdir("pickled_classifiers"):
        os.makedirs("pickled_classifiers")
        
    joblib.dump(
        model,
        "pickled_classifiers/classifier_{}.pkl".format(datetime.date.today()),
        compress = 3
    )


if classifier_config.pickled_classifier: #If we're using a stored classifier
    classif_pipe = joblib.load(classifier_config.pickled_classifier)
else: #If we're creating/using a new classifier
    classif_pipe = trainClassifier()
    
#TODO: Create some code to benchmark the classifier's precision
#And store the precision info as classifier's metada, for later usage

#That's probably gonna require some code to create training and testing data