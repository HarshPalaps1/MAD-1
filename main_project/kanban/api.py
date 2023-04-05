from .import api
from flask_restful import Resource,fields, marshal_with,reqparse,HTTPException,abort
from . import db
from .Models import Card, Member,List
from fastapi import Response,status
from datetime import datetime

#**********************************************************(For Member api controller )***********************************************
member_body={"id":fields.Integer,
             "name": fields.String,
             "email":fields.String}


create_member_parser = reqparse.RequestParser()
create_member_parser.add_argument('name')
create_member_parser.add_argument('email')
create_member_parser.add_argument('password')        


update_member_parser = reqparse.RequestParser()
update_member_parser.add_argument('password')  

class allmemberAPI(Resource):
    @marshal_with(member_body)
    def get(self):
        member=Member.query.all()
        if member:
            return member,status.HTTP_200_OK
        else :     
            abort(status.HTTP_404_NOT_FOUND,message="not found")






class memberAPI(Resource):




    @marshal_with(member_body)
    def get(self,Name):
        member=Member.query.filter_by(name=Name).all()

        if  member:
            return member

        else :      
            abort(status.HTTP_404_NOT_FOUND,message="not found")
    

    def post(self):
        args = create_member_parser.parse_args() 
        Name = args.get("name", None)
        Email = args.get("email", None)
        Password = args.get("password", None)
        member_already=Member.query.filter_by(email=Email).first()

        if Name is None:
            abort(status.HTTP_400_BAD_REQUEST,message="name not found")
        elif Name == (" ") or Name==(""):
            abort(status.HTTP_400_BAD_REQUEST,message="give proper name")    
 
        elif Email is None:
            abort (status.HTTP_400_BAD_REQUEST,message='Email not found')

        elif "@" not in Email:
            abort (status.HTTP_400_BAD_REQUEST,message="in valid Email  format")
        elif member_already:
            abort(status.HTTP_400_BAD_REQUEST,message="Member with same email already exist")
        else:
            new_member = Member(name=Name,email=Email,password=Password)
            db.session.add(new_member)
            db.session.commit()
            return {"message":"Member account created!!!"} ,status.HTTP_201_CREATED

    def delete(self,Name):
        member=Member.query.filter_by(name=Name).first()
        
        if member:
            list=List.query.filter_by(member_id=member.id).first()
            if list:
                abort(status.HTTP_409_CONFLICT, message="Member have lists first delete it !!!")
                #return member.id
            else:
                db.session.delete(member)
                db.session.commit()
                return f" {member.name} account deleted"
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='Member of this name does\'nt exist')

    def put(self,Name):
        member=Member.query.filter_by(name=Name).first()
        if member:
                args=update_member_parser.parse_args()
                Password = args.get("password", None)
                member.passward=Password
                db.session.commit()
                return f" {member.name} account updated"
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='Member of this name does\'nt exist')



            
#**********************************************************(For List api controller )***********************************************
list_body={ "id": fields.Integer,
            "list_name":fields.String,
            "date":fields.DateTime}



create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('list_name')
create_list_parser.add_argument('member_name') 


update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('new_list_name') 


class ListsAPI(Resource):
    @marshal_with(list_body)
    def get(self):
        list=List.query.all()
        if list:
            return  list,status.HTTP_200_OK
        else :     
            abort(status.HTTP_404_NOT_FOUND,message="no listfound")

class alllistAPI(Resource):  
    @marshal_with(list_body)
    def get(self,Name):
        member=Member.query.filter_by(name=Name).first()

        
        if member:
            list=List.query.filter_by(member_id=member.id).all()
            if  list:
                return list
            else :
                abort(status.HTTP_404_NOT_FOUND,message="list not found")
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='Member of this name does\'nt exist')



 
class listAPI(Resource):
    @marshal_with(list_body)
    def get(self,list_name_input):
        list=List.query.filter_by(list_name=list_name_input).all()

        if  list:
                return list

        else :
            abort(status.HTTP_404_NOT_FOUND,message="not found")

    def post(self):
        args = create_list_parser.parse_args() 
        list_name_input= args.get('list_name', None)
        member_name = args.get('member_name', None)
        list=List.query.filter_by(list_name=list_name_input).first()
        member=Member.query.filter_by(name=member_name).first()
        if  not member:
            abort(status.HTTP_404_NOT_FOUND,message=f"Member of this name not found")
        elif list:
            abort(status.HTTP_400_BAD_REQUEST,message=f"List with same {list.list_name} already exist")  
        else:
            user_of_list=Member.query.filter_by(name=member_name).first()
            

            new_list = List(list_name=list_name_input,date=datetime.now(),member_id=user_of_list.id)
            db.session.add(new_list)
            db.session.commit()
            return {"message":"new list created!!!"} ,status.HTTP_201_CREATED


    def delete(self,list_name_input):
        list=List.query.filter_by(list_name=list_name_input).first()
        
        if list:
            card=Card.query.filter_by(list_id=list.id).first()
            if card:
                abort(status.HTTP_409_CONFLICT,message="list have cards first delete it !!!")
                #return card.id
            else:
                db.session.delete(list)
                db.session.commit()
                return f" {list.list_name} list deleted"
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='list of this name does\'nt exist')    

    def put(self,list_name_input):
        list=List.query.filter_by(list_name=list_name_input).first()
        if list:
                args=update_list_parser.parse_args()
                new_Title = args.get("new_list_name", None)
                list.list_name=new_Title
                db.session.commit()
                return f" {list_name_input} list  name updated to {list.list_name}"
        else:
           

            abort (status.HTTP_400_BAD_REQUEST,message="list of this name does\'nt exist")
    

#**********************************************************(For Card api controller )***********************************************
card_body={ "id": fields.Integer,
            "task":fields.String,
            "content":fields.String,
            "have_date":fields.Boolean,
            "status":fields.Boolean,
            "due_date":fields.String
            }



create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('task')
create_card_parser.add_argument('content') 
create_card_parser.add_argument('due_date')
create_card_parser.add_argument('list_name')





update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('status') 


change_card_parser = reqparse.RequestParser()
change_card_parser.add_argument('task') 
change_card_parser.add_argument('content')
change_card_parser.add_argument('due_date')  




class CardsAPI(Resource):
    @marshal_with(card_body)
    def get(self):
        card=Card.query.all()
        if card:
            return card,status.HTTP_200_OK
        else :     
            abort(status.HTTP_404_NOT_FOUND,message="no listfound")

 
class cardAPI(Resource):
   
    @marshal_with(card_body)
    def get(self,Task):

        one_Card=Card.query.filter_by(task=Task).first()
        if  one_Card:
            return one_Card
        else:
            abort(status.HTTP_404_NOT_FOUND,message="not found")


    def post(self):
        args = create_card_parser.parse_args() 
        Task= args.get('task',None)
        Content= args.get("content", None)
        Due_date= args.get("due_date", None)
        List_name=args.get("list_name", None)

        card_of_list=List.query.filter_by(list_name=List_name).first()
        card_already=Card.query.filter_by(task=Task).first()

        if card_already:
            abort(status.HTTP_400_BAD_REQUEST,message=f"card with same {card_already.task} already exist") 
        else:    
            now_date=datetime.now()
            form_due_time=datetime.strptime(str(Due_date),"%Y-%m-%d %H:%M:%S")

            new_card = Card(task=Task,content=Content,have_date=(form_due_time>now_date),form_date=now_date,status=0,due_date=form_due_time,list_id=card_of_list.id)
            db.session.add(new_card)
            db.session.commit()
            return {"message":"card is created!!!"} ,status.HTTP_201_CREATED

    def patch(self,Task):
        one_Card=Card.query.filter_by(task=Task).first()
        if one_Card:
            if one_Card.have_date==0:
                abort (status.HTTP_400_BAD_REQUEST,message='Due date of task is crossed')
            if one_Card.status==1:
                abort (status.HTTP_400_BAD_REQUEST,message='already Update is done')
            else:
                args=update_card_parser.parse_args()
                new_status = args.get("status", None)
                one_Card.status=int(new_status)
                now_date=datetime.now()
                time=datetime.strptime(str(now_date),"%Y-%m-%d %H:%M:%S.%f")
                one_Card.done_date=time
                db.session.commit()
                return "Card is  updated"
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='card of this task does\'nt exist')



    def put(self,Task):
        card=Card.query.filter_by(task=Task).first()
        if card:
                args=change_card_parser.parse_args()
                new_task = args.get("task", None)
                new_content = args.get("content", None)
                new_due_date = args.get("due_date", None)
                card.task=new_task
                card.content=new_content
                time=datetime.strptime(str(new_due_date),"%Y-%m-%d %H:%M:%S")
                card.due_date=time
                db.session.commit()
                return f" card got  modified "
        else:
            abort (status.HTTP_400_BAD_REQUEST,message="list of this name does\'nt exist")


    def delete(self,Task):
        one_Card=Card.query.filter_by(task=Task).first()
        
        if one_Card:
            db.session.delete(one_Card)
            db.session.commit()
            return f"  card name {one_Card.task}  deleted"
        else:
            abort (status.HTTP_400_BAD_REQUEST,message='Member of this name does\'nt exist')  
