from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()
connection_string = f"postgresql+psycopg2://korep:@localhost:5432/korep"
engine = create_engine(connection_string)
Session = sessionmaker(engine)
metadata_obj = MetaData()

class Books(Base):
    __tablename__ = 'books_orm'
    
    book_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(Date, nullable=False)
    date_deleted = Column(Date, nullable=True)


    def __str__(self):
        return f'«{self.title}» - {self.author} ({self.published})'
    
    
class Borrows(Base):
    __tablename__ = 'borrows_orm'
    
    borrow_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books_orm.book_id"))
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=True)
    user_id = Column(String, primary_key=True)

# Base.metadata.create_all(engine)