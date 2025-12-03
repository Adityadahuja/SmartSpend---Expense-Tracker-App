from app.models import Expense
from datetime import datetime
from sqlalchemy import func
from app import db

class AssistantService:
    @staticmethod
    def get_analysis(user):
        if not user:
            return None
            
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        # Calculate total expenses for current month
        total_expenses = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user.id,
            func.extract('month', Expense.date) == current_month,
            func.extract('year', Expense.date) == current_year,
            Expense.type == 'expense'
        ).scalar() or 0.0
        
        # Calculate savings
        savings = user.salary - total_expenses
        
        # Generate advice
        advice = AssistantService.generate_advice(user.salary, total_expenses, savings)
        
        return {
            'total_expenses': total_expenses,
            'savings': savings,
            'advice': advice
        }
    
    @staticmethod
    def generate_advice(salary, expenses, savings):
        if salary == 0:
            return "Please set your monthly salary in your profile to get personalized advice."
            
        savings_ratio = (savings / salary) * 100
        
        if savings_ratio < 0:
            return "Warning: You have exceeded your monthly salary! Try to cut down on non-essential expenses."
        elif savings_ratio < 10:
            return "You are saving less than 10% of your income. Consider reviewing your budget."
        elif savings_ratio < 20:
            return "Good job! You are saving a decent amount. Aim for 20% for better financial health."
        else:
            return "Excellent! You are managing your finances very well. Keep it up!"
