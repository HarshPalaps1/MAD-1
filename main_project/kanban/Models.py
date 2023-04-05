from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func\



#**********************************************************(Member database )***********************************************

class Member(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))




    Lists=db.relationship("List",backref="member")



#**********************************************************(List database )***********************************************
class List(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    list_name=db.Column(db.String(2000),nullable=False)
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    member_id=db.Column(db.Integer(), db.ForeignKey("member.id"), nullable=False)



    cards=db.relationship("Card" ,backref="list" ,cascade = "all, delete")

    


#**********************************************************(Card database )***********************************************
class Card(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    task=db.Column(db.String(30),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    have_date=db.Column(db.Boolean(),default=True)
    status=db.Column(db.Boolean(),default=False)
    form_date=db.Column(db.Integer(),nullable=True)
    due_date=db.Column(db.Integer(),nullable=False)
    done_date=db.Column(db.Integer(),nullable=True)




    list_id=db.Column(db.Integer(), db.ForeignKey("list.id"), nullable=False)













