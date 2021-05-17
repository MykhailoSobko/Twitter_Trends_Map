from flask import Flask, render_template, request, redirect
from user_db import User, Authenticator, UserAlreadyExistsError, IncorrectCredentials, TooManyTracked
from api_work import get_json
from trends_adt import *


app = Flask(__name__)

auth = Authenticator()


@app.route("/")
def homepage():
    current_user = auth.current_user
    print(current_user)
    if current_user:
        return render_template("index.html", current_user=current_user.username)
    else:
        return render_template("index.html", current_user=current_user)


@app.route("/regform")
def regform():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        print(password)
        auth.register(username, password)
        return redirect("/")
    except UserAlreadyExistsError:
        return redirect("/error/userex")


@app.route("/loginform")
def loginform():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        print(password)
        auth.login(username, password)
        print(auth.current_user)
        return redirect("/")
    except IncorrectCredentials:
        return redirect("/error/incor")


@app.route("/trendslist/<country>", methods=["GET"])
def trends_list(country):
    trends = []
    jsn = get_json(country)
    adt = TrendsADT(jsn["trends"], jsn["as_of"], jsn["locations"])
    filtered_trends = adt._trends
    for tre in filtered_trends:
        trends.append(tre)
    print(trends)
    return render_template("trends.html", trends=trends, country=country)


@app.route("/addtrack/<country>/<name>", methods=["POST", "GET"])
def addtrack(country, name):
    print(name)
    if request.method == "POST":
        if not auth.current_user:
            return redirect("/error/track")
        try:
            auth.current_user.add_trend_to_track(name, country)
        except TooManyTracked:
            return redirect("/error/too_many_tracked")
    return render_template("added.html", trend=name)


@app.route("/deltrack/<country>/<name>", methods=["POST", "GET"])
def deltrack(country, name):
    if request.method == "POST":
        if not auth.current_user:
            return redirect("/error/track")
        auth.current_user.delete_trend_from_tracked(name, country)
    return render_template("deleted.html", trend=name)


@app.route("/profile", methods=["GET"])
def display_info():
    current_user = auth.current_user
    print(current_user)
    print(current_user.username)
    userinfo = current_user.get_all_info_for_user(current_user.username)
    print(userinfo)
    return render_template("profile.html", user_trends=userinfo[0], username=current_user.username, tracked=userinfo[2])


@app.route("/error/<name>")
def show_error(name):
    return render_template("tracking_error.html", name=name)

@ app.route("/map")
def map():
    return render_template("choose_country.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)

