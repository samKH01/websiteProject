from datetime import datetime
from website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    familyname = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    adress = db.Column(db.String(64), index=True, unique=True)
    phone = db.Column(db.Integer(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='email', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_content = db.Column(db.LargeBinary, nullable=False)
    qr_code = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    email_id = db.Column(db.Integer, db.ForeignKey('email.id'))

    def __repr__(self):
        return f'<Document {self.file_name}>'
