import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from os import path
from flask_login import LoginManager
from .Models import Member
from flask_restful import  Resource,Api



def website_app():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    app=Flask(__name__)
    app.config['SECRET_KEY']="harshpalaps1"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, "myalldata.sqlite3")
    db.init_app(app)
    api=Api(app)


        
    from .Controllers import controller
    from .Accounts  import account
    from .Stat import stat

    from .api import memberAPI,listAPI,cardAPI,allmemberAPI,alllistAPI,ListsAPI,CardsAPI


    
    app.register_blueprint(controller,url_prefix="/")
    app.register_blueprint(account,url_prefix="/")
    app.register_blueprint(stat,url_prefix="/")

    api.add_resource(allmemberAPI,"/api/member/all",)
    api.add_resource(memberAPI,"/api/member/<Name>","/api/member",)
    api.add_resource(ListsAPI,"/api/list/all",)
    api.add_resource(alllistAPI,"/api/member/<Name>/list",)
    api.add_resource(listAPI,"/api/list/<list_name_input>","/api/list")
    api.add_resource(CardsAPI,"/api/card/all",)
    api.add_resource(cardAPI,"/api/card/<Task>","/api/card","/api/card/all")
  


    if not path.exists("WEBSITE/myalldata.sqlite3"):
        db.create_all(app=app)


    login_manager = LoginManager() #initiated class
    login_manager.login_view="/login" # place where it take if not logged in 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Member.query.get(int(id))





    return app,api