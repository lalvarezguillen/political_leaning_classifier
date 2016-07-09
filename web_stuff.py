import classifier
try:
    from tools import scrapers
except:
    from .tools import scrapers
from flask import Flask, request, abort, render_template
import json


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("predict.html")

@app.route('/predict', methods = ['POST'])
def handle_input():
    request.data = json.loads(request.data)
    print("request content: {}".format(request.data))
    if request.data:
        #Just pass the statement to the classifier
        statement = request.data["statement"]
        return json.dumps(predict(statement))
    else:
        return abort(400, "Did not receive a statement")



def predict(statement_to_predict):
    predictions = classifier.classif_pipe.predict_proba([statement_to_predict])
    result = {
        "left":predictions[0][0],
        "right":predictions[0][1]
    }
    return result

def predictFBUser(fb_username):
    posts = scrapers.getFbPostsFrom(fb_username)
    if len(posts)> 0:
        predictions = classifier.predictListOfStatements(classifier.classif_pipe, posts)
        return predictions
