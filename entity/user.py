
from app import db
from utils import util

from sqlalchemy import Column, Integer, String
    
class User(db.Model):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), unique=True, nullable=False)
    role = Column(String(10), nullable=True)

    def __init__(self, username=None, password=None, role=None):
        self.username = username
        self.password = password
        self.role = role

    def getPassword(self):
        return self.password
    
    def setPassword(seld, password):
        seld.password = password
    
    def getUsername(self):
        return self.username
    
    def setUsername(self, username):
        self.username = username

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role