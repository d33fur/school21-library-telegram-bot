from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from database.models import Books, Borrows

user = "korep"
 
connection_string = f"postgresql+psycopg2://{user}:@localhost:5432/{user}" # changelog: port changed from 5432
 
Base = declarative_base()
 
class DatabaseConnector:
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self, db_name):
        meta = MetaData()
        meta.reflect(self.engine) 

    def process_string_case(self, input_string):
        return input_string.lower().capitalize()
    
    def add(self, title, author, published):
        try:
            book = Books(
                title = self.process_string_case(title), 
                author = self.process_string_case(author), 
                published = published, 
                date_added = datetime.now()
            )

            self.session.add(book)
            self.session.commit()
            return book.book_id
        except:
            self.session.rollback()
            return False
 
    def delete(self, title, author, published):
        try:
            book = self.session.query(Books).filter(Books.title == title, Books.author == author, Books.published == published, Books.date_deleted == None).first()
            borrow = self.session.query(Borrows).filter(Borrows.book_id == book.book_id).first()

            if book == None:
                return False
            if borrow:
                return False
            else:
                book.date_deleted = datetime.now()
                self.session.commit()
                return True
        except:
            self.session.rollback()
            return False

    def list_books(self):
        return self.session.query(Books).filter(Books.date_deleted == None).all()

    def get_book(self, title, author, published):
        book = self.session.query(Books).filter(
            Books.title == self.process_string_case(title), 
            Books.author == self.process_string_case(author), 
            Books.published == published
        ).first()

        if book == None:
            return None

        return book

    def borrow(self, title, author, published, user_id):
        book = self.get_book(title, author, published)

        if self.session.query(Borrows).filter(
            Borrows.user_id == user_id, 
            Borrows.date_end == None).count() > 0:
            return False
        
        if self.session.query(Borrows).filter(Borrows.book_id == book.book_id, Borrows.date_end == None).count() > 0:
            return False

        new_borrow = Borrows(book_id = book.book_id, user_id=user_id, date_start=datetime.now())

        try:
            self.session.add(new_borrow)
            self.session.commit()
            return new_borrow.borrow_id
        except:
            self.session.rollback()
            return False

    def get_borrow(self, user_id):
        borrow = self.session.query(Borrows).filter(Borrows.user_id == user_id, Borrows.date_end == None)

        if borrow == None:
            return None
        
        return borrow.borrow_id

    def retrieve(self, user_id):
        borrow = self.session.query(Borrows).filter(Borrows.user_id == str(user_id), Borrows.date_end == None)

        if borrow != None:
            borrow = borrow.first()
        else:
            return False
        
        try:
            borrow.date_end = datetime.now()
            self.session.commit()
            book = self.session.query(Books).filter(Books.book_id == borrow.book_id).first()
            return book # todo return book
        except:
            return False
