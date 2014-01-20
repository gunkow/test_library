# from app import db

from app.models import Base, Author, Book, author_book
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

if __name__ == '__main__':
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(engine)
    dbs = Session()

    moses = Author('moses')
    moses.books.append(Book('ten commandments'))
    moses.books.append(Book('seven sins'))

    bible = Book('bible')
    god = Author('god')
    god.books.append(bible)
    moses.books.append(bible)

    Constitution = Book('Constitution')
    Yanukovich_Viktor = Author('Yanukovich Viktor')
    Pulup_Orluk = Author('Pulup Orluk')
    Constitution.authors.append(Pulup_Orluk)
    Yanukovich_Viktor.books.append(Constitution)
    Yanukovich_Viktor.books.append(bible)

    dbs.add(moses)
    dbs.add(bible)
    dbs.add(Constitution)
    dbs.commit()
