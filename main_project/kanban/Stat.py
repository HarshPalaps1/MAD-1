from flask import Blueprint,render_template
from flask_login import login_required,  current_user
from datetime import datetime
from .Models import Card,List
from . import db 


  

stat=Blueprint("stat",__name__)

@stat.route('list/view/<list_id>',methods=["GET"])
@login_required
def list_view(list_id):
    list=List.query.filter_by(id=list_id).first()
    cards=Card.query.filter_by(list_id=list_id).all()
    pie_card={}
    time_line=[]
    pie_card['Task']='Hours per Day'
    total_task=0
    done_task=0
    pending_task=0
    undone_task=0
    for i in cards:
        time_line.append(i)
        total_task+=1
        if i.status==1:
            done_task+=1
            done_time=i.done_date
            form_done_time=datetime.strptime(str(done_time),"%Y-%m-%d %H:%M:%S.%f")
            issued_time=i.form_date
            form_issued_time=datetime.strptime(str(issued_time),"%Y-%m-%d %H:%M:%S.%f")
            time=form_done_time-form_issued_time
            pie_card[i.task]=time.total_seconds()
                   
        else:
            
            now=datetime.now()
            form_now_time=datetime.strptime(str(now),"%Y-%m-%d %H:%M:%S.%f")
            issued_time=i.form_date
            form_issued_time=datetime.strptime(str(issued_time),"%Y-%m-%d %H:%M:%S.%f")
            time= form_now_time-form_issued_time
            pie_card[i.task]=time.total_seconds()

        if i.have_date:
            if i.status==1:
                pass
            else:
             pending_task+=1
        else:
            undone_task+=1

      
           
          
        
 




    
    
    return render_template('view.html',
                            data2=time_line,
                            data=pie_card,
                            id=list_id,
                            List=list,
                            Cards=cards,
                            member=current_user,
                            a=pie_card,
                            Total_task=total_task,
                            Done_task=done_task,
                            Pending_task=pending_task,
                            Undone_task=undone_task)
    #return {"ans":f"{time_line}"}



