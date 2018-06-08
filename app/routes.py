from flask import render_template, session, redirect, request, url_for
from app import app, db
from app.extention import login_required
from app.models import User, Board, Comment


@app.route('/')
@login_required
def index():
	boards = Board.query.all()
	return render_template('index.html', boards=boards)


@app.route('/new_board', methods=["GET","POST"])
@login_required
def new_board():
    if request.method == "POST":
		
        board = Board(board_name=request.form.get("board_name"), user_id=session["user_id"])
        db.session.add(board)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("new_board.html")	


@app.route('/<board_id>', methods=["GET"])
@login_required
def view_board(board_id):
	board = Board.query.filter_by(id=board_id).first_or_404()
	comments = board.comments	
	return render_template("view_board.html", board=board, comments=comments)


@app.route('/<board_id>/add_comment', methods=["GET", "POST"])
@login_required
def add_comment(board_id):
	if request.method == "POST":
		comment = Comment(text=request.form.get("comment_text"), user_id=session["user_id"], board_id=board_id)
		db.session.add(comment)
		db.session.commit()
		return redirect('/%s' % board_id)
	else:
		return render_template("add_comment.html")	




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        if user is None or not user.check_pass(request.form.get("password")):
            return redirect(url_for('login'))

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
        user.set_pass(request.form.get("password"))
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")           