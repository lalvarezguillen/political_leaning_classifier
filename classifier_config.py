import os

#classfier to use. If none trains a new classifier
pickled_classifier = ""


#training dataset
db_path = os.path.join(
    os.path.dirname(__file__),
    "dataset.db"
)


#Some network config
app_port = 8080
app_host = "0.0.0.0"