from flask import Blueprint,render_template,request,flash,url_for,redirect
from .Models import Member
from flask_login import login_user, login_required, logout_user, current_user
from . import db

account=Blueprint("account",__name__)



#**********************************************************(For login function)***********************************************
@account.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method=="POST":
        Name=request.form.get("name")
        Email=request.form.get("email")
        Password=request.form.get("password")
        member=Member.query.filter_by(email=Email).first()



        if member:
            if Password==member.password:
                flash("successfully loggedin ." , category="success")
                login_user(member,remember=True)
                return redirect(url_for("controller.home"))

            else:
                flash("Incorrect password.", category="error")

        else:
                flash("member do not exist.",category="error")
    return render_template('login.html',member=current_user)

    


#**********************************************************(For signup function)***********************************************
@account.route("/Sign_Up", methods = ['GET', 'POST'])
def Sign_Up():
    if(request.method=='POST'):
        Name = request.form.get('name')
        Email = request.form.get('email')
        Password = request.form.get('password')
        Confirm_Password = request.form.get('confirm_password')

        member=Member.query.filter_by(email=Email).first()
        
        if member:
            flash("already exist",category="error")
        elif "@" not in Email :
            flash('invalid email.', category='error')
        elif len(Name) < 2:
            flash('Name  must be greater than 1 character.', category='error')
        elif Password != Confirm_Password:
            flash('Passwords don\'t match.', category='error')
        elif len(Password) < 5:
            flash('Password must be at least 5 characters.', category='error')
        else:
            new_member=Member(name=Name,email=Email ,password=Password )
            db.session.add(new_member)
            db.session.commit()
            login_user(current_user, remember=True)
            flash("Account created" , category="success")

            redirect(url_for('controller.home'))

    return render_template('sign_up.html',
                            member=current_user)

#**********************************************************(For logout function)***********************************************
@account.route("/logout")
@login_required 
def logout():
    logout_user()
    return  redirect(url_for("account.login"))