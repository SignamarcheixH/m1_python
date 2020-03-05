import os
from flask import Flask, render_template,  url_for, json, request
import pandas as pd
import re
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from stop_words import get_stop_words
from joblib import dump, load

warnings.filterwarnings('ignore')


app = Flask(__name__)

def initClf():
	data = loadData() 
	clf = make_pipeline(
    	TfidfVectorizer(stop_words=get_stop_words('en')),
    	OneVsRestClassifier(SVC(kernel='linear', probability=True))
	)
	clf = clf.fit(X=data['tweet'], y=data['class'])
	dump(clf, 'tweet_classifier.joblib')


def loadData():
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	data_url = os.path.join(SITE_ROOT, "static", "labeled_data.csv")
	df = pd.read_csv(data_url, usecols=['class', 'tweet'])
	df_sample = df.sample(n=1000)
	df_sample['tweet'] = df_sample['tweet'].apply(lambda tweet: re.sub('[^A-Za-z]+', ' ', tweet.lower()))
	return df_sample

@app.route('/')
@app.route('/index.html')
@app.route('/tweet/')
def index():
	return render_template('index.html')

@app.route('/tweet_results',  methods=['POST'])
def analyseTweet():
	tweets = loadData();
	clf = load('tweet_classifier.joblib');
	tweet = request.form['tweet'];
	tweet_array = [tweet]
	probas_results = clf.predict_proba(tweet_array);
	#probas_results = probas_results.apply(lambda percent: percent * 100 )
	return render_template('results.html', probas=probas_results, tweet=tweet)

if __name__ == "__main__":
	initClf();
	app.run(debug = True)
