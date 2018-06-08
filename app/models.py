from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30),index=True, unique=True)
	hash_pwd = db.Column(db.String(120))
	boards = db.relationship('Board', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_pass(self, password):
		self.hash_pwd = generate_password_hash(password)

	def check_pass(self, password):
		return check_password_hash(self.hash_pwd, password)	


class Board(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	board_name = db.Column(db.String(50),index=True, unique=True)
	create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Board {}>'.format(self.board_name)