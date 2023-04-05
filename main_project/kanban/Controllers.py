from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,  current_user
from datetime import datetime
from .Models import Card,List
from . import db
from datetime import timedelta
controller=Blueprint("controller",__name__)



#**********************************************************(For home page controller )***********************************************
@controller.route('/',methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        list_name_input=request.form.get("sticker")
        list=List.query.filter_by(list_name=list_name_input[1:]).first()

        if list:
            #return {'a':list}
            flash("list with this title already exist",category="error")
        else:    
            if list_name_input==" ":
                flash("shell can\'t be null ",category="error")
            else:
                new_List=List(list_name=str(list_name_input)[1:],date= datetime.now(),member_id=current_user.id)
                db.session.add(new_List)
                db.session.commit()

                lists=List.query.filter_by(member_id=current_user.id).all()
            
                return render_template('/home.html',
                                        List=lists, 
                                        member=current_user)


    list=List.query.filter_by(member_id=current_user.id).all()

    return render_template('home.html',
                             List=list,
                             member=current_user)


#**********************************************************(For deleting list controller )***********************************************

@controller.route('/delete/list/<list_id>',methods=["GET","POST"])
@login_required
def list_delete(list_id):
    list_delete=List.query.get(list_id) # collect  card to delete with help of card id we get form
    Member_id=list_delete.member_id #using that card to get its list id
    db.session.delete(list_delete)
    db.session.commit()

    lists=List.query.filter_by(member_id=Member_id).all()


    return redirect(url_for('controller.home',
                                List=lists,
                                member=current_user))

#**********************************************************(For list page to change title of list controller )***********************************************
@controller.route('list/update/<list_id>',methods=["POST"])
@login_required
def update_card(list_id):
    updated_title=request.form.get("change_title")
    if updated_title==" ":
        flash(" Change list title shell can\'t be null ",category="error")
    else:
        list=List.query.get(list_id)
        list.list_name=updated_title[1:]
        db.session.commit()
    
        
        return redirect(url_for('controller.get_cards_of_list',
                                    home_list_id=list_id,
                                    member=current_user))

    return redirect(url_for('controller.get_cards_of_list',
                                    home_list_id=list_id,
                                    member=current_user))




#**********************************************************(For list page controller )***********************************************


@controller.route('/list/<home_list_id>',methods=["GET"])
@login_required
def get_cards_of_list(home_list_id):

    cards=Card.query.filter_by(list_id=home_list_id).all()
    list=List.query.filter_by(id=home_list_id).first()

    current_date= datetime.now() 
    now_date=datetime.strptime(str(current_date),"%Y-%m-%d %H:%M:%S.%f")  
    

    for card in cards:
        check_time=datetime.strptime(str(card.due_date),'%Y-%m-%d %H:%M:%S')
        if card.status==0:
            if check_time > now_date :
                card.have_date=1
                db.session.commit()
            else:
                card.have_date=0
                db.session.commit()   
        else: 
            pass

    return render_template('list.html',
                            id=home_list_id,
                            List=list,
                            Cards=cards,
                            member=current_user)
    
#**********************************************************(For adding card in list  controller )***********************************************

@controller.route('/list/<list_id>',methods=["POST"])
@login_required
def post_in_card_of_list(list_id):

    Task=request.form.get("task")
    Content=request.form.get("content")
    Due_date=request.form.get("due_date")

    check_date= datetime.now() 
    given_date=datetime.strptime(str(Due_date),'%Y-%m-%dT%H:%M')
    auto_date=datetime.strptime(str(check_date),"%Y-%m-%d %H:%M:%S.%f")
    new_5=given_date+timedelta(days=5)

    card=Card.query.filter_by(task=Task[1:]).first()  
    list=List.query.filter_by(id=list_id).first()   


    if card:
        flash("card with this task already exist",category="error")
    else:                                                            
        if Task==" ":
            flash("shell can\'t be null ",category="error")
        elif Content==' ':
            flash("content shell can\'t be null ",category="error")
        elif auto_date>given_date:
            flash("Invalid Due Date and Time",category="error")
                
        else: 
            new_card=Card(task=Task[1:],list_id=list_id,content=Content[1:],form_date=auto_date,due_date=new_5,have_date=(given_date>auto_date))
            db.session.add(new_card)
            db.session.commit()


            list=List.query.filter_by(id=list_id).first()


            return redirect(url_for('controller.get_cards_of_list',
                                    home_list_id=list_id,
                                    List=list,
                                    member=current_user,
                                    time=auto_date))

    return redirect(url_for('controller.get_cards_of_list',
                                home_list_id=list_id,
                                List=list,
                                member=current_user,
                                time=auto_date)) 
   
 
#**********************************************************(For changing card status controller )***********************************************

@controller.route('/update/card/<card_id>',methods=["GET","POST"])
@login_required
def card_update(card_id):
    card_to_update=Card.query.get(card_id)
    if card_to_update.status==1:
        flash("Invalid Due Date and Time",category="error")

    else:

        list_id=card_to_update.list_id
        time_done=datetime.now()
        formated_done_time=datetime.strptime(str(time_done),"%Y-%m-%d %H:%M:%S.%f")
        card_to_update.done_date=formated_done_time
        card_to_update.status=1
        db.session.commit()
    
        list_id=card_to_update.list_id

        return redirect(url_for('controller.get_cards_of_list',
                                    home_list_id=list_id,
                                    member=current_user))



    return redirect(url_for('controller.get_cards_of_list',
                                home_list_id=list_id,
                                member=current_user))     


@controller.route('/delete/card/<card_id>',methods=["GET","POST"])
@login_required
def card_delete(card_id):
    card_delete=Card.query.get(card_id) 
    list_id=card_delete.list_id 
    db.session.delete(card_delete)
    db.session.commit()


    return redirect(url_for('controller.get_cards_of_list',
                                home_list_id=list_id,
                                member=current_user)) 





#**********************************************************(For moving card from one list to another list controller )***********************************************

@controller.route('/move/<id>',methods=["POST"])
@login_required
def movement(id):
    card_task=request.form.get("card_name")
    list_title=request.form.get("list_name")

    if card_task==" ":
        flash("Card name shell can\'t be null ",category="error")
    if list_title=="":
        flash("List shell can\'t be null ",category="error")
        return redirect(url_for('controller.get_cards_of_list',home_list_id=id,member=current_user))
    card=Card.query.filter_by(task=str(card_task[1:])).first()
    list=List.query.filter_by(list_name=str(list_title)[1:]).first()
    card.list_id=list.id
    db.session.commit()

    #return {"ans":card_task}
    return redirect(url_for('controller.get_cards_of_list',home_list_id=id,member=current_user)) 


