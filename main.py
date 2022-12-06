# Lucas Bubner, 2022
from flask import Flask, render_template, redirect, request
from os import environ
from sqlite3 import connect
from functools import wraps
from waitress import serve

app = Flask(__name__)
sql = connect("posts.db", check_same_thread=False)
posts = sql.cursor()
logged_in = False


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not logged_in:
            print("> debug | login_required check failed.")
            return redirect("/login")
        return f(*args, **kwargs)
    return check


@app.route('/')
def index():
    rows = posts.execute("SELECT id, title, content, img, imgheight FROM posts").fetchall()
    print("> debug | fetched sql tables containing post information.")
    return render_template("index.html",
                           logged_in = logged_in,
                           posts = rows)

   
@app.route("/addpost", methods=['GET', 'POST'])
@login_required
def addpost():
    if request.method == "POST":
        data = [
            request.form.get("title"),
            request.form.get("content"),
            request.form.get("image"),
            request.form.get("imageheight")
        ]
        posts.execute("INSERT INTO posts(title, content, img, imgheight) VALUES(?,?,?,?)", data)
        print("> debug | updating db with new data...")
        sql.commit()
        return redirect("/")
    else:
        return render_template("add.html", logged_in = logged_in)


@app.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete(id):
    if request.method == "POST":
        posts.execute("DELETE FROM posts WHERE id = ?", (id,))
        print("> debug | removing database id {}".format(id))
        sql.commit()
    return redirect("/")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def editpost(id):
    if request.method == "POST":
        post = posts.execute("SELECT id, title, content, img, imgheight FROM posts WHERE id =?", (id,)).fetchone()
        
        if not (title := request.form.get("title")): 
            title = post[1]
            
        if not (content := request.form.get("content")): 
            content = post[2]
            
        if not (image := request.form.get("image")): 
            image = post[3]
            
        if not (imageheight := request.form.get("imageheight")): 
            imageheight = post[4]
            
        data = [
            title,
            content,
            image,
            imageheight,
            id
        ]
        
        posts.execute("UPDATE posts SET title = ?, content = ?, img = ?, imgheight = ? WHERE id = ?", data)
        print("> debug | updating db with new data...")
        sql.commit()
        return redirect("/")
    else:
        toedit = posts.execute("SELECT id, title, content, img, imgheight FROM posts WHERE id = ?", (id,)).fetchone()
        print("> debug | fetching edits for a post...")
        return render_template("edit.html", logged_in = logged_in, post = toedit)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global logged_in
    if request.method == 'POST':
        password = request.form.get("password")

        if password == environ['password']:
            logged_in = True
            print("> debug | logged in successfully")
            return redirect("/")

        print("> debug | failed login")
        return render_template("login.html",
                               incorrect = True)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    print("> debug | logged out successfully")
    return redirect("/")


if __name__ == '__main__':
    print("> APP INIT | running on http://127.0.0.1:8080/")
    serve(app, host='0.0.0.0', port=8080)
