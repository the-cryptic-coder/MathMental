from flask import *
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3
import random
import time

app=Flask(__name__)
app.secret_key = "something unique"
conn = sqlite3.connect('mathmental')
c = conn.cursor()

flag1=False

@app.route('/')
def hello_world():
    conn = sqlite3.connect('mathmental')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users1(
              username text,
              email text,
              passhash text
              )''')
    conn.commit()
    c.execute('''
              CREATE TABLE IF NOT EXISTS ascore(
              username text,
              score integer
              )''')
    conn.commit()
    c.execute('''
              CREATE TABLE IF NOT EXISTS mscore(
              username text,
              score integer
              )''')
    conn.commit()
    if "username" in session:
        return render_template("logged_in_home.html")
    else:
        return render_template("home.html")

@app.route('/login', methods=["POST","GET"])
def login():
    if "username" in session:
        return render_template("logged_in_home.html")
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        conn = sqlite3.connect('mathmental')
        c = conn.cursor()
        c.execute("SELECT * FROM users1")
        user_list=c.fetchall()

        for u in user_list:
            if u[0]==username:
                if check_password_hash(u[2], password):
                    session["username"]=username
                    return render_template("logged_in_home.html")
            else:
                return "<h1>Invalid Credentials</h1>"

    else:
        return render_template("login.html")

@app.route('/register', methods=["POST","GET"])
def register():
    flag1=False
    if "username" in session:
        return render_template("logged_in_home.html")
    if request.method=="POST":
        conn = sqlite3.connect('mathmental')
        c = conn.cursor()
        username=request.form["username"]
        user_email=request.form["email"]
        password= request.form["password"]
        pass_hash=generate_password_hash(password)
        if username.strip() == "" or len(password)<8:
            return "<h1>Password Or Username Invalid</h1>"
        conn = sqlite3.connect('mathmental')
        c = conn.cursor()
        c.execute("SELECT * FROM users1")
        user_list=c.fetchall()
        for u in user_list:
            if u[0]==username:
                flag1=True
                return "<h1>Account already exists, please log in</h1>"
            if u[1]==user_email:
                flag1=True
                return "<h1>Account already exists, please log in</h1>"

        if flag1==False:
            c.execute("insert into users1 (username, email, passhash) values (?, ?, ?)",
                      (username, user_email, pass_hash))
            conn.commit()
            session["username"]=username
            return render_template("logged_in_home.html")
    else:
        return render_template("register.html")

@app.route('/logout', methods=["POST","GET"])
def logout():
    if "username" in session:
        session.pop("username")
        return render_template("home.html")
    else:
        return "<h1>Login To Logout</h1>"

@app.route('/about', methods=["POST","GET"])
def about():
    if "username" in session:
        return render_template("about.html", flag=False)
    else:
        return render_template("about.html", flag=True)

@app.route('/multiplication', methods=["POST","GET"])
def multiplication():
    if request.method == "GET":
        if "username" in session:
            global randomlist
            global randomlist2
            global start_time
            randomlist = random.sample(range(0, 30), 10)
            randomlist2 = random.sample(range(0, 30), 10)
            start_time=time.time()
            return render_template("multiplication.html", flag=False, randomlist=randomlist, randomlist2=randomlist2)
        else:
            return render_template("error.html", flag=True)
    else:
        flag2=False
        final_time=time.time()-start_time
        answers=0
        n=int(request.form["number"])
        n1=int(request.form["number1"])
        n2=int(request.form["number2"])
        n3=int(request.form["number3"])
        n4=int(request.form["number4"])
        n5=int(request.form["number5"])
        n6=int(request.form["number6"])
        n7=int(request.form["number7"])
        n8=int(request.form["number8"])
        n9=int(request.form["number9"])
        user_answers=[]
        user_answers1=[n,n1,n2,n3,n4,n5,n6,n7,n8,n9]
        for i in range(len(user_answers1)):
            if user_answers1[i] == '':
                user_answers.append(-1)
            else:
                user_answers.append(int(user_answers1[i]))
        correct_answers=[]
        for x in range(10):
            correct_answers.append(randomlist[x]*randomlist2[x])
        for i in range(len(user_answers)):
            if user_answers[i]==correct_answers[i]:
                answers+=1

        final_time=round(final_time)
        score=(100-final_time)*answers
        if final_time>99:
            score=answers
        conn = sqlite3.connect('mathmental')
        c = conn.cursor()
        c.execute("SELECT * FROM mscore")
        scores=c.fetchall()
        for i in scores:
            if i[0]==session["username"]:
                flag2=True
                if score>i[1]:
                    c.execute("UPDATE mscore SET score = ? WHERE username= ?", (score, session["username"]))
                    conn.commit()

        if flag2==False:

            c.execute("insert into mscore (username, score) values (?, ?)",
                      (session["username"], score))
            conn.commit()


        return render_template("results.html",answers=answers, final_time=final_time, score=score)

@app.route('/addition', methods=["POST","GET"])
def addition():

    if request.method == "GET":
        if "username" in session:
            global randomlist
            global randomlist2
            global start_time
            randomlist = random.sample(range(0, 100), 10)
            randomlist2 = random.sample(range(0, 100), 10)
            start_time=time.time()
            return render_template("addition.html", flag=False, randomlist=randomlist, randomlist2=randomlist2)
        else:
            return render_template("error.html", flag=True)
    else:
        flag2=False
        final_time=time.time()-start_time
        answers=0
        n=request.form["number"]
        n1=request.form["number1"]
        n2=request.form["number2"]
        n3=request.form["number3"]
        n4=request.form["number4"]
        n5=request.form["number5"]
        n6=request.form["number6"]
        n7=request.form["number7"]
        n8=request.form["number8"]
        n9=request.form["number9"]
        user_answers=[]
        user_answers1=[n,n1,n2,n3,n4,n5,n6,n7,n8,n9]
        for i in range(len(user_answers1)):
            if user_answers1[i] == '':
                user_answers.append(-1)
            else:
                user_answers.append(int(user_answers1[i]))
        correct_answers=[]
        for x in range(10):
            correct_answers.append(randomlist[x]+randomlist2[x])
        for i in range(len(user_answers)):
            if user_answers[i]==correct_answers[i]:
                answers+=1

        final_time=round(final_time)
        score=(100-final_time)*answers
        if final_time>99:
            score=answers
        conn = sqlite3.connect('mathmental')
        c = conn.cursor()
        c.execute("SELECT * FROM ascore")
        scores=c.fetchall()
        for i in scores:
            if i[0]==session["username"]:
                flag2=True
                if score>i[1]:
                    c.execute("UPDATE ascore SET score = ? WHERE username= ?", (score, session["username"]))
                    conn.commit()

        if flag2==False:

            c.execute("insert into ascore (username, score) values (?, ?)",
                      (session["username"], score))
            conn.commit()


        return render_template("results.html",answers=answers, final_time=final_time, score=score)


@app.route('/leaderboard', methods=["POST","GET"])
def leaderboard():
    if "username" in session:
        conn=sqlite3.connect("mathmental")
        c=conn.cursor()

        c.execute("SELECT * FROM ascore")
        list1=c.fetchall()
        newList = sorted((age, name) for name, age in list1)
        list2 = [(name, age) for age, name in newList]
        users=[]
        scores=[]
        for i in newList:
            users.append(i[1])
            scores.append(i[0])
        length=len(users)
        users.reverse()
        scores.reverse()
        return render_template("leaderboard.html", users=users, scores=scores, length=length)
    else:
        return render_template("error.html")

@app.route('/mleaderboard', methods=["POST","GET"])
def mleaderboard():
    if "username" in session:
        conn=sqlite3.connect("mathmental")
        c=conn.cursor()

        c.execute("SELECT * FROM mscore")
        list1=c.fetchall()
        newList = sorted((age, name) for name, age in list1)
        list2 = [(name, age) for age, name in newList]
        users=[]
        scores=[]
        for i in newList:
            users.append(i[1])
            scores.append(i[0])
        length=len(users)
        users.reverse()
        scores.reverse()
        return render_template("mleaderboard.html", users=users, scores=scores, length=length)
    else:
        return render_template("error.html")


if __name__ == "__main__":
    app.run()