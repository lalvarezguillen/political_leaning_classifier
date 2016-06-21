from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from .tools.database_stuff import db


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
