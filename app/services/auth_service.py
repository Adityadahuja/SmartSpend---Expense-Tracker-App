from app import db
from app.models import User

class AuthService:
    @staticmethod
    def register_user(name, email, password, salary=0.0):
        if User.query.filter_by(email=email).first():
            return None  # User already exists
        
        user = User(name=name, email=email, salary=salary)
        user.set_password(password)
        db.session.add(user)
        db.session.flush() # Get user ID

        # Create initial salary income transaction
        if salary > 0:
            from app.models import Category, Expense
            from datetime import datetime
            
            salary_category = Category.query.filter_by(name='Salary').first()
            if not salary_category:
                salary_category = Category(name='Salary')
                db.session.add(salary_category)
                db.session.flush()
            
            expense = Expense(
                user_id=user.id,
                category_id=salary_category.id,
                amount=salary,
                date=datetime.utcnow(),
                payment_method='Bank Transfer', # Default
                note='Initial Salary Registration',
                type='income'
            )
            db.session.add(expense)

        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))
