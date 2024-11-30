
from my_app import db

from sqlalchemy import Column, Integer, String


class WordToeic(db.Model):

    __tablename__ = "word_toeic"
    id = Column(Integer, primary_key=True)
    word = Column(String(40), nullable=False)
    transliteration = Column(String(40), nullable=False)
    mean1 = Column(String(80), nullable=False)
    mean2 = Column(String(80), nullable=True)
    mean3 = Column(String(80), nullable=True)
    mean4 = Column(String(80), nullable=True)
    mean5 = Column(String(80), nullable=True)

    def __init__(self, word=None, transliteration=None, mean1=None, mean2=None, mean3=None, mean4=None, mean5=None):
        self.word = word
        self.transliteration = transliteration
        self.mean1 = mean1
        self.mean2 = mean2
        self.mean3 = mean3
        self.mean4 = mean4
        self.mean5 = mean5

    # Getter and Setter for word
    def get_word(self):
        return self.word

    def set_word(self, value):
        self.word = value

    # Getter and Setter for transliteration
    def get_transliteration(self):
        transliteration = self.transliteration.replace("-", "\'")
        return transliteration

    def set_transliteration(self, value):
        self.transliteration = value

    # Getter and Setter for mean1
    def get_mean1(self):
        return self.mean1

    def set_mean1(self, value):
        self.mean1 = value

    # Getter and Setter for mean2
    def get_mean2(self):
        return self.mean2

    def set_mean2(self, value):
        self.mean2 = value

    # Getter and Setter for mean3
    def get_mean3(self):
        return self.mean3

    def set_mean3(self, value):
        self.mean3 = value

    # Getter and Setter for mean4
    def get_mean4(self):
        return self.mean4

    def set_mean4(self, value):
        self.mean4 = value

    # Getter and Setter for mean5
    def get_mean5(self):
        return self.mean5

    def set_mean5(self, value):
        self.mean5 = value

    def __repr__(self):
        return f"<WordToeic(id={self.id}, word={self.word}, transliteration={self.transliteration}, " \
               f"mean1={self.mean1}, mean2={self.mean2}, mean3={self.mean3}, " \
               f"mean4={self.mean4}, mean5={self.mean5})>"

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "transliteration": self.get_transliteration(),
            "mean1": self.mean1,
            "mean2": self.mean2,
            "mean3": self.mean3,
            "mean4": self.mean4,
            "mean5": self.mean5,
        }
