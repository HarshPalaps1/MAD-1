from kanban import  website_app


app,api=website_app()



if __name__=="__main__":
    app.run(debug=True)