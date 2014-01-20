from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class SearchForm(Form):
    book = TextField('book title like:')
    author = TextField('author name like:') # , validators=[Required()])


class EditForm(Form):
    title = TextField('Title:',  [Required()])

class AddAuthorForm(Form):
    author_name = TextField('Edit name:',  [Required()])



