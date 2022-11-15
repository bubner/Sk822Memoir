# Lucas Bubner, 2022
from flask import Flask, render_template, redirect, request
from os import environ

app = Flask(__name__)
logged_in = False


@app.route('/')
def index():
    return render_template("index.html", logged_in=logged_in)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global logged_in
    if request.method == 'POST':
        password = request.form.get("password")

        if password == environ['password']:
            logged_in = True
            return redirect("/")

        return render_template("login.html", incorrect=True)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return redirect("/")


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
