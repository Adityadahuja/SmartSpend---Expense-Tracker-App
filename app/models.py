from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    salary = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f'<Category {self.name}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    payment_method = db.Column(db.String(64))
    note = db.Column(db.String(140))
    type = db.Column(db.String(20), default='expense') # 'income' or 'expense'
    
    category = db.relationship('Category')

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category.name if self.category else 'Uncategorized',
            'amount': self.amount,
            'date': self.date.isoformat(),
            'payment_method': self.payment_method,
            'note': self.note,
            'type': self.type
        }

    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    subject = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.subject} from {self.email}>'
