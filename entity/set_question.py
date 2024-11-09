
from my_app import db

from sqlalchemy import Column, Integer, String

import enum
from sqlalchemy import Enum


class ResultStatus(enum.Enum):
    PASS = "PASS"
    FAILED = "FAILED"
    UNTESTED = "UNTESTED"


class SetQuestion(db.Model):

    __tablename__ = "set_question"
    id = Column(Integer, primary_key=True)
    name_set = Column(Integer, nullable=False)
    list_question = Column(String(500), nullable=False)
    result = db.Column(Enum(ResultStatus),
                       default=ResultStatus.UNTESTED, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name_set, list_question, result=ResultStatus.UNTESTED, user_id=None):
        self.name_set = name_set
        self.list_question = list_question
        self.result = result
        self.user_id = user_id

    # Getter and Setter for name_set
    def get_name_set(self):
        return self.name_set

    def set_name_set(self, value):
        self.name_set_ = value

    # Getter and Setter for list_question
    def get_list_questions(self):
        return self.list_question

    def set_list_questions(self, value):
        self.list_question = value

    def get_result_status(self):
        return self.result

    def set_result_status(self, value):
        if isinstance(value, ResultStatus):
            self.result = value
        else:
            raise ValueError("Invalid result status")

    # Getter and Setter for user_id
    def get_user_id(self):
        return self.user_id

    def set_user_id(self, value):
        self.user_id = value
