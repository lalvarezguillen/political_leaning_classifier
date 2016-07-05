import pytest
import web_stuff
import sklearn
import classifier
try:
    from .tools import scrapers
except:
    from tools import scrapers


def test_predict():
    prediction = web_stuff.predict("This is a test statement, and it should return a dictionary")
    assert type(prediction) is dict
    
def test_generate_balanced_dataset():
    dataset1, dataset2 = classifier.generateBalancedDataset()
    assert len(dataset1) == len(dataset2)
    

def test_remove_numbers():
    assert "My sentence without numbers" == classifier.removeNumbers("My1 sentence3 witho0ut numb3ers")
    
def test_train_classifier():
    trained_classifier = classifier.trainClassifier()
    assert type(trained_classifier) == sklearn.pipeline.Pipeline
    
def test_fb():
    assert hasattr(scrapers.fb, "get")
    
def test_twitter():
    assert hasattr(scrapers.api, "search")
    
def test_remove_urls():
    removed_urls = scrapers.removeUrls("This is Trump's twitter account https://twitter.com/realDonaldTrump")
    assert removed_urls == "This is Trump's twitter account "
    
def test_is_relevant_statement():
    statement = "Elected officials must focus on protecting the environment for our future generations, not enable polluters to curb regulations. #StopTPPNow"
    assert scrapers.isRelevantStatement(statement)