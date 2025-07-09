from flask import Flask,render_template,request,redirect #imporing
from flask_sqlalchemy import SQLAlchemy #importing
from flask_migrate import Migrate #importing for migration

#installing 
#importing
#initializing
#if needed configuration
#integrating 

app=Flask(__name__)  #initialization

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootcamp.db'  #configuring the database

db=SQLAlchemy() #initializing 

db.init_app(app)  #integrating the database with the app


migrate = Migrate(app,db)



#ORM -- Object Relational Mapping 
#Mapping relational databases with python classes (objects)

#for each table in the database there will be a class in python
#every object of that class is a row in the table


app.app_context().push()  #to push the app context for database operations
 


class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    is_admin = db.Column(db.Boolean,default=False)  #to check if the user is admin or not


db.create_all()  #to create all the tables in the database



#there is no function written here to treat the request 


#if user comes into the path "/" then server doesnt know how 
#to treat the request because there is npthing defined

#flask-by default tries to find all the html pages that is mentioned in the app
#in the templates folder

@app.route('/')  #decorator
def home():
    return render_template('hello.html')

@app.route('/login', methods=['GET'])  #by default only allows the GET request
def login():
    return render_template('login.html')

@app.route('/login_user',methods=['POST'])  #to handle the POST request
def login_user():
        formusername = request.form['username']
        formpassword = request.form['password']
        
        already_exist = Users.query.filter_by(username=formusername).first()

        print(already_exist)

        if already_exist:
             print(already_exist.username)
             print(already_exist.password)
             print(already_exist.is_admin)
             if already_exist.password == formpassword:
                print("Password is correct")
                return redirect('/dashboard')
             else:
                print("Password is incorrect")
                return redirect('/login')
        else:
            print("User does not exist")
                #redirect to signup page
            return redirect('/signup')

             
@app.route('/dashboard',methods=['GET'])
def dashboard():
     return render_template('dashboard.html')


@app.route('/signup',methods=['GET','POST'])  #to handle the GET and POST request
def signup():
     if request.method=="GET":
            return render_template('signup.html')
     else:
        formusername= request.form.get('username')
        formpassword = request.form.get('password')
        
        #all the tables in the database are the classes in the application
        #every row of that table is an object of that class

        #User----> User class ---> object of user classs will have properties of the user
        #id,username,password,is_admin

        #check if the username already exists in the database
        already_exist = Users.query.filter_by(username=formusername).first()

        if already_exist:
            print("Username already exists")
            return redirect('/signup')
        else:
             #you need to create an object of that classs in order to add inside that table
            print("Username is available")
            new_user = Users(username=formusername,password=formpassword)
            db.session.add(new_user)
            db.session.commit()
            print("User added successfully")
            return redirect('/login')




if __name__ == '__main__':
    #before running the app i need ot check tht admin is rhere or not 
    admin_already_exist = Users.query.filter_by(username='admin',is_admin=True).first()
    if not admin_already_exist:
        print("Admin user does not exist, creating one")
        admin_user = Users(username='admin',password='admin',is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully")
    app.run(debug=True) #use debug mode



#





