from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import app

Base = declarative_base()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app.db'

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    books = relationship("Book", secondary=lambda: author_book, backref="authors")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all(dbsesion):
        return dbsesion.query(Author).all()

    @staticmethod
    def get_byId(id, dbsesion):
        return dbsesion.query(Author).filter(Author.id == id).first()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column('title', String(64))

    def __init__(self, title):
        self.title = title

    @staticmethod
    def get_byId(id, dbsesion):
        return dbsesion.query(Book).filter(Book.id == id).first()

    @staticmethod
    def get_all(dbsesion):
        return dbsesion.query(Book).all()

    @staticmethod
    def get_byTitle(title, dbsesion):
        return dbsesion.query(Book).filter(Book.title.like('%%%s%%' % (title) )).all()

    @staticmethod
    def get_byTitleAuthor(title, author, dbsesion):
        return dbsesion.query(Book).\
            join(Book.authors).\
            filter(Author.name.like('%%%s%%' % (author) )).\
            filter(Book.title.like('%%%s%%' % (title) )).all()


author_book = Table('author_book', Base.metadata,
    Column('author_id', Integer, ForeignKey("author.id"),
           primary_key=True),
    Column('book_id', Integer, ForeignKey("book.id"),
           primary_key=True)
)

