from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///study.db', echo=True)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()


class WordList(Base):
    __tablename__ = "word_lists"
    id = Column(Integer, primary_key=True)

    name = Column(String)

    entries = relationship("WordListEntry")

    def __repr__(self):
        return "<WordList(id={}, name={}>".format(self.id, self.name)


class WordListEntry(Base):
    __tablename__ = "word_list_entries"
    id = Column(Integer, primary_key=True)
    word = Column(String)

    word_list_id = Column(Integer, ForeignKey('word_lists.id'))
    list = relationship("WordList", back_populates="entries")

    __table_args__ = (
        UniqueConstraint('word_list_id', 'word', name='_word_list_word_uc'),
    )

    def __repr__(self):
        return "<WordListEntry(id={}, word={}, word_list_id={}>".format(self.id, self.word, self.word_list_id)

def create_tables():
    Base.metadata.create_all(engine)
