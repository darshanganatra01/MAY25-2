from flask import Flask,render_template,request,redirect,flash,session #imporing
from flask_sqlalchemy import SQLAlchemy #importing
from flask_migrate import Migrate #importing for migration

#installing 
#importing
#initializing
#if needed configuration
#integrating 

app=Flask(__name__)  #initialization

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootcamp.db'  #configuring the database
app.config['SECRET_KEY']='peppernsalt'


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

class Albums(db.Model):
    a_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    album_name=db.Column(db.String(100),unique=True,nullable=False)

class Songs(db.Model):
    s_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name = db.Column(db.String(100),unique=True,nullable=False)
    singer_name = db.Column(db.String(100),nullable=False)

    #F.K
    album_id = db.Column(db.Integer,db.ForeignKey(Albums.a_id),nullable=False)

#albums
#<song 1> --- > <album 1>

#songs
#<album 1> ---> <song 1>

    albums = db.relationship('Albums',backref=db.backref('songs',lazy=True))

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
                session['username']= already_exist.username  #to store the username in the session
                session["is_admin"]=already_exist.is_admin
                return redirect('/dashboard')
             else:
                print("Password is incorrect")
                flash("password is incorrect") 
                return redirect('/login')
        else:
            print("User does not exist")
                #redirect to signup page
            return redirect('/signup')

             
@app.route('/dashboard',methods=['GET'])
def dashboard():
    username=session.get('username')
    is_admin=session.get('is_admin')
    #session['username']
    #1.either you can store the is_admin value in the session
    #2.in the dashboard route you can fetch the user details
    albums = Albums.query.all()
    songs=Songs.query.all()
    if is_admin:
        print("User is admin")
        return render_template('admin_dashboard.html',name=username,jinjalbums=albums,jinjasongs=songs)
    return render_template('dashboard.html',name=username,jinjalbums=albums,is_admin=is_admin,jinjasongs=songs) #songs

#query.all()
#pass it to the template
#for loop inside the template

#create_user
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
            flash("Username already exists")
            return redirect('/signup')
        else:
             #you need to create an object of that classs in order to add inside that table
            print("Username is available")
            new_user = Users(username=formusername,password=formpassword)
            db.session.add(new_user)
            db.session.commit()
            print("User added successfully")
            return redirect('/login')


#create albums 
#i need to update albums
#i need to delete albums 
#i need to read the albums 

#only admin can create update delete everything user is only allowed
#to see things not change them 

@app.route('/create_album',methods=['GET','POST'])

#get ---> give the user the create album form 
#post ---> check if it exists or not
#then if it doesnt exist then create it in the database
def create_album():
    if request.method == 'GET':
        return render_template('create_album.html')
    else:
        formalbumname = request.form.get('albumname')

        #check if the album already exists in the database
        album_already_exist = Albums.query.filter_by(album_name=formalbumname).first()
        if album_already_exist:
            flash("album already exists please use a different name")
            return redirect('/create_album')
        else:
            print("album name available")
            new_album = Albums(album_name=formalbumname)
            db.session.add(new_album)
            db.session.commit()
            print("album created successfully")
            return redirect('/dashboard')
        

@app.route('/update_album/<album_id>',methods=['GET','POST'])
def update_album(album_id):
    is_admin = session['is_admin']
    if not is_admin:
        print("You are not authorized to update albums")
        return redirect('/login')
    if request.method=='GET':
        album_id  = int(album_id)  #convert the album_id to integer
        album_name = Albums.query.filter_by(a_id=album_id).first().album_name
        return render_template('update_album.html',album_id=album_id,jinjaalbum_name=album_name)
    else:
        updatedalbumname=request.form.get('albumname')

        #we have the albumid
        #first check that the album id which we have
        #corresponds to some album in the database
        #find that album
        #assign the new name to the old name

        album_to_update = Albums.query.filter_by(a_id=album_id).first()
        if album_to_update:
            print("Album Found")

            #ROCK ----> POP
            #ROCK ----> Dance --> problem
            #we need to check that the updated album name doesnt exist

            check_albumname = Albums.query.filter_by(album_name=updatedalbumname).first()

            if check_albumname:
                flash("the name theat you gave to change is not avaialable")
                return redirect('/update_album/'+str(album_id))
            
            else:
                print("the name is available")

                album_to_update.album_name = updatedalbumname
                db.session.commit()
                print("Album updated successfully")
                return redirect('/dashboard')
        else:
            print("Album not found")
            return redirect('/dashboard')
        

@app.route('/delete_album/<album_id>',methods=['GET'])
def delete_album(album_id):
    album_id = int(album_id)
    album_to_delete = Albums.query.filter_by(a_id=album_id).first()

    songs_in_album = Songs.query.filter_by(album_id=album_id).first()

    if songs_in_album:
        db.session.delete(songs_in_album)
        db.session.commit()
        print("Songs in the album deleted successfully")
    
    if album_to_delete:
        db.session.delete(album_to_delete)  #to delete the album from the database
        db.session.commit()
        print("Album deleted successfully")
        return redirect('/dashboard')
    else:
        print("Album not found")
        return redirect('/dashboard')


@app.route('/create_song',methods=['GET','POST'])

#get ---> give the user the create album form 
#post ---> check if it exists or not
#then if it doesnt exist then create it in the database
def create_song():
    if request.method == 'GET':
        return render_template('create_song.html')
    else:
        formsongname = request.form.get('songname')
        formsingername = request.form.get('singername')
        formalbumid = request.form.get('albumid')

        #check if the album already exists in the database
        song_already_exist = Songs.query.filter_by(song_name=formsongname).first()
        if song_already_exist:
            print("song already exists please use a different name")
            return redirect('/create_song')
        else:
            print("Song name available")
            new_song = Songs(song_name=formsongname,singer_name=formsingername,album_id=formalbumid)
            db.session.add(new_song)
            db.session.commit()
            print("song created successfully")
            return redirect('/dashboard')







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







#Reading 
#making seperate dashboards for user and admin
#defining relationships more and connecting everything
#creating songs 
#deleting things effectively witout integrity errors
#Flash




#create a effective dropdown menu for admin albums
#updating and deleting songs 
#plots
#search 
#basic github



#albums --- songs


#lots ---- spots
#create a lot there is a number of spots property
