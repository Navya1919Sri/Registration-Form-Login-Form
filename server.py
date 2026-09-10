
import sqlite3
from flask import Flask,render_template,request,redirect
app=Flask(__name__)
@app.route("/")
def Create_database():
    #connect to database
    connection=sqlite3.connect("users.db")
    # store database in some object
    cursor=connection.cursor()
    # write query using that object
    cursor.execute("""create table if not exists users(
    id integer primary key autoincrement,
    fullname text not null,
    username text unique not null,
    password text not null)""")
    # commit query
    connection.commit()
    # close connection 
    connection.close() 
    return render_template("reg.html")
 
@app.route("/register", methods=["POST"])
def register():
    fullname= request.form["fullname"]
    username= request.form["username"]
    password= request.form["password"]
    connection=sqlite3.connect("users.db")
    cursor=connection.cursor() 
    cursor.execute("""
            INSERT INTO users(fullname,username,password)
            VALUES(?,?,?)
            """,(fullname,username,password)
            )      
    connection.commit()
    connection.close()
    return redirect("/login")    

@app.route("/login", methods=["GET"])  
def login_page():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
    username=request.form["username"]
    password=request.form["password"]
    connection=sqlite3.connect("users.db")
    cursor=connection.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """,(username,password))
    user=cursor.fetchone()
    connection.close()
    if user:
        return "<h2>login successful</h2><p>welcome,"+ username +"!</p>"
    else:
        return "<h2>login failed</h2><p>welcome or password is incorrect</p>"
if __name__=="__main__":
    app.run(debug=True)    