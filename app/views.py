from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, engine
from forms import SearchForm, EditForm, AddAuthorForm
from sqlalchemy.orm import sessionmaker
from app.models import Book, Author
import json
# @app.before_first_request
# def init():
#     g.dbs = sessionmaker(engine)()

@app.before_request
def before_request():
    g.dbs = sessionmaker(engine)()
#
# @app.after_request
# def after_request():
#     g.dbs.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    form = SearchForm()
    results = None
    if request.method == 'POST' and form.validate_on_submit():
        book = request.form['book']
        author = request.form['author']
        results = Book.get_byTitleAuthor(book, author, g.dbs)

        # flash('book: %s author: %s' % (books, author))
    return render_template('search_books.html', form=form, results=results)

@app.route('/edit_books_and_authors', methods=['GET', 'POST'])
def edit_books_and_authors():
    books = Book.get_all(g.dbs)
    authors = Author.get_all(g.dbs)
    book_form = EditForm()
    author_form = AddAuthorForm()
    return render_template('edit_books_and_authors.html', books=books, authors=authors,  form=book_form, author_form=author_form)

@app.route('/authors_of_book', methods=['GET'])
def authors_of_book():
    book_id = request.args['id']
    book = Book.get_byId(book_id, g.dbs)
    author_ids = []
    for author in book.authors:
        author_ids.append(author.id)
    json = dict(id=book_id)
    return jsonify(book_id=book.id, book_title=book.title, author_ids=author_ids)

@app.route('/update_books', methods=['POST'])
def update_books():
    title = request.form['title']
    authors = request.form['authors']
    data = json.loads(authors)
    book_id = request.form['id']
    if book_id == 'new_book':
        book = Book(title)
    else:
        book = Book.get_byId(book_id, g.dbs)
        del book.authors[:]
        book.title = title
    for it in data:
        book.authors.append(Author.get_byId(it, g.dbs))
    g.dbs.add(book)
    g.dbs.commit()
    return 'success'

@app.route('/update_authors', methods=['POST'])
def update_authors():
    author_id = request.form['active_author_id']
    author_name = request.form['author_name']
    if author_id == 'new_author':
        author = Author(author_name)
    else:
        author = Author.get_byId(author_id, g.dbs)
        author.name = author_name
    g.dbs.add(author)
    g.dbs.commit()
    return redirect(url_for('edit_books_and_authors'))

@app.route('/delete_instance', methods=['POST'])
def delete_instance():
    instance_type = request.form['type']
    id = request.form['id']
    if instance_type == 'book':
        instance = Book.get_byId(id, g.dbs)
    elif instance_type == 'author':
        instance = Author.get_byId(id, g.dbs)
    else:
        return 'wtf?'
    g.dbs.delete(instance)
    g.dbs.commit()
    return 'ok'
