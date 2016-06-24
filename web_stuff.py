import classifier
from flask import Flask, request, abort
import json


app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def handle_input():
    """{
        "url":"", #try to obtain text content of the tweet/post,
        "statement": "Venezuelans go back home"
    }"""
    if "url" in request:
        if "facebook.com" in request["url"]:
            #Obtain the post
            statement = obtainPostContent(request["url"])
        elif "twitter.com" in request["url"]:
            #obtain the tweet
            statement = obtainTweetContent(request["url"])
    elif "statement" in request:
        "Just pass the statement to the classifier"
        statement = request["statement"]
        
    if not statement: return abort(400, "Did not receive an statement :(")
    return json.dumps(predict(statement))


    #Obtain the text content of the tweet or FB post, probably using the TW/FB api
    
def predict(statement_to_predict):
    predictions = classifier.classif_pipe.predict_proba([statement_to_predict])
    result = {}
    for k, label in enumerate(classifier.classif_pipe.classes_):
        result[label] = "{}%".format(predictions[k]*100)
    return result
    
def obtainPostContent(url):
    return

def obtainTweetContent(url):
    return
