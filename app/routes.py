from flask import session, redirect, request, jsonify, make_response
from app import app, db
from app.extention import login_required, can_comments, can_likes, validator
from app.models import User, Board, Comment, Likes


@app.route('/', methods=["GET"])
@login_required
def index():
    boards = Board.query.all()
    all_boards = []
    for board in boards:
        all_boards.append({'id': board.id, 'board_name': board.board_name})

    return make_response(jsonify(all_boards), 200)


@app.route('/new_board', methods=["POST"])
@login_required
def new_board():
    board = request.get_json()

    error = validator('board', board)
    if error:
        return jsonify(error)

    add_board = Board(board_name=board.get("board_name"), user_id=session["user_id"])
    db.session.add(add_board)
    db.session.commit()

    return redirect("/")


@app.route('/<board_id>', methods=["GET"])
@login_required
def view_board(board_id):
    boards = Board.query.filter_by(id=board_id).first_or_404()
    board = {'id': boards.id, 'author': boards.author.username, 'create_date': boards.create_date}
    all_comment = []
    comments = boards.comments
    for comment in comments:
        all_comment.append({'id': comment.id, 'author': comment.author.username, 'text': comment.text})
    likes = Likes.query.filter_by(board_id=board_id).count()
    return make_response(jsonify({'board': board, 'comments': all_comment, 'likes': likes}), 201)


@app.route('/<board_id>/add_comment', methods=["POST"])
@login_required
def add_comment(board_id):
    comment = request.get_json()

    error = validator('comment', comment)
    if error:
        return jsonify(error)

    new_comment = Comment(text=comment.get("comment_text"), user_id=session["user_id"], board_id=board_id)

    if can_comments():
        db.session.add(new_comment)
        db.session.commit()
        session["count_comments"] -= 1
        return redirect('/%s' % board_id)
    else:
        return jsonify({'error': 'You have reached your message limit in hour'})


@app.route('/<board_id>/likes_board', methods=["POST"])
@login_required
def likes_board(board_id):
    like = Likes(user_id=session["user_id"], board_id=board_id)
    if can_likes():
        db.session.add(like)
        db.session.commit()
        session["count_likes"] -= 1
        return redirect('/%s' % board_id)
    else:
        return jsonify({'error': 'You have reached your likes limit in hour'})


@app.route("/login", methods=["POST"])
def login():
    session.clear()
    user = User.query.filter_by(username=request.form.get("username")).first()

    if user is None or not user.check_pass(request.form.get("password")):
        return jsonify({'error': 'Error authorization'})

    session["user_id"] = user.id

    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    new_user = request.get_json()
    user = User(username=new_user["username"])
    user.set_pass(new_user["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify()


@app.route("/logout")
def logout():
    session.clear()
