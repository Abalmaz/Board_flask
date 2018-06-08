from flask import render_template, session, redirect, request
from app import app
from app.extention import login_required
from app.models import User

@app.route('/')
@login_required
def index():
	user = {'username': 'Jane'}
	return render_template('index.html', title='Home', user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        if user is None or not user.check_pass(request.form.get("password")):
            return apology("invalid username and/or password", code=403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        user = User(username=request.form.get("username"))
        user.set_password(request.form.get("password"))
        db.sessionadd(user)
        db.session.commit()

        session["user_id"] = result

        return redirect("/")

    else:
        return render_template("register.html")        