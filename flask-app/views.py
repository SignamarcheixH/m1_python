import os
from flask import Flask, render_template,  url_for, json


app = Flask(__name__)


def loadData():
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "books.json")
	data = json.load(open(json_url))
	return data

@app.route('/')
@app.route('/index.html')
@app.route('/books/all/')
@app.route('/books/')
def index():
	books = loadData()
	return render_template('index.html', books=books)

@app.route('/books/title/<string:book_title>')
def singleBook(book_title):
	books = loadData()
	matching_books = [book for book in books if book_title.lower() in book['title'].lower()]
	return render_template('single.html', books=matching_books)


@app.route('/books/author/<string:book_author>')
def getByAuthor(book_author):
	books = loadData()
	matching_books = [book for book in books if book_author.lower() in ''.join(book['authors']).lower()]
	return render_template('single.html', books=matching_books)


if __name__ == "__main__":
    app.run(debug = True)