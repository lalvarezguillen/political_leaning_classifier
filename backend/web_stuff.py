import classifier
#import Flask

#@map_to_url("/predict", method=post)
#def handle_input():
    #flask.request.data should contain the url of a tweet or FB post
    #Grab that url, decide if it's FB or TW
    #Obtain the text content of the tweet or FB post, probably using the TW/FB api
    #Pass it to a predict fnction
    #Expect the return result of predict
    #return the prediction back to the user
    
def predict(statement_to_predict):
    predictions = classifier.classif_pipe.predict_proba([statement_to_predict])
    result = {}
    for k, label in enumerate(classifier.classif_pipe.classes_):
        result[label] = "{}%".format(predictions[k]*100)
    return result
    