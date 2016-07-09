from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import numpy as np

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer

from tools.database_stuff import db
import classifier_config
import os
import datetime
import random
import re

__codename__ = "PyBernie"

def generateBalancedDataset():
    """ slices the dataset, to obtain a balanced dataset """
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

def removeNumbers(document):
    """ preprocessor that removes digits from the statements """
    return re.sub("[0-9]+", "", document)

def trainNeuralNetwork():
    """ Trains a neural network with the current dataset """
    print("Generating training and testing data....")
    statements, labels = generateBalancedDataset()

    """ Vectorize the statements """
    vect = TfidfVectorizer(
        analyzer="word", ngram_range=(1,2),
        stop_words="english", max_df=0.70, min_df=3
    )
    print("Vectorizing the statements and labels...")
    statements = vect.fit_transform(statements)
    n_input_neurons = len(vect.vocabulary_)

    """ vectorize the labels """
    v_labels = []
    for label in labels:
        if label == "left":
            v_labels.append(np.array([1,0]))
        elif label == "right":
            v_labels.append(np.array([0,1]))

    labels = v_labels

    """ Build the dataset """
    print("building the dataset...")
    ds = ClassificationDataSet(
        n_input_neurons, 2,
        nb_classes=2, class_labels=["left", "right"]
    )

    for k,statement in enumerate(statements):
        ds.addSample(statement.toarray()[0], labels[k])

    """ Split training and testing data """
    training_data, testing_data = ds.splitWithProportion(0.1)

    """ Build the neural network accordingly """
    nn = buildNetwork(
        n_input_neurons,
        int(float(n_input_neurons)/2),
        2
    )

    """ Build the nn trainer """
    trainer = BackpropTrainer(nn, dataset=ds, verbose=True)

    return (trainer, vect, nn, testing_data)


def trainClassifier():
    """ Trains a classifier with the current dataset """
    classif_pipe = Pipeline([
        ("vect", TfidfVectorizer(analyzer="word", ngram_range=(1,3), stop_words="english", max_df=0.70, min_df=3, preprocessor=removeNumbers )),
        ("clf", MultinomialNB(alpha=0.1))
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


def predictListOfStatements(pipe, statements):
    """ Predicts the political leaning of a group of statements """
    predictions = pipe.predict_proba(statements)
    left = sum([x[0] for x in predictions])/len(predictions)
    right = sum([x[1] for x in predictions])/len(predictions)
    return {
        "left": left,
        "right": right
    }


def storeClassifier(model):
    """ Stores the trained classifier in hard drive, to make it available for later use """
    if not os.path.isdir("pickled_classifiers"):
        os.makedirs("pickled_classifiers")

    joblib.dump(
        model,
        "pickled_classifiers/classifier_{}.pkl".format(datetime.date.today()),
        compress = 3
    )

def show_most_informative_features(n=30):
    """Shows the most informative features, separated by target class"""
    vectorizer = classif_pipe.named_steps["vect"]
    clf = classif_pipe.named_steps["clf"]
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2)


if classifier_config.pickled_classifier: #If we're using a stored classifier
    classif_pipe = joblib.load(classifier_config.pickled_classifier)
else: #If we're creating/using a new classifier
    classif_pipe = trainClassifier()
