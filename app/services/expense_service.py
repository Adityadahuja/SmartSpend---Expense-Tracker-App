from app import db
from app.models import Expense, Category
from app.algorithms import merge_sort_expenses, aggregate_by_category, compute_daily_prefix_sum
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
import io

class ExpenseService:
    @staticmethod
    def create_expense(data, user_id):
        expense = Expense(
            user_id=user_id,
            category_id=data.get('category_id'),
            amount=float(data.get('amount')),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d'),
            payment_method=data.get('payment_method'),
            note=data.get('note'),
            type=data.get('type', 'expense')
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def update_expense(expense_id, data, user_id):
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        if expense:
            expense.category_id = data.get('category_id')
            expense.amount = float(data.get('amount'))
            expense.date = datetime.strptime(data.get('date'), '%Y-%m-%d')
            expense.payment_method = data.get('payment_method')
            expense.note = data.get('note')
            expense.type = data.get('type', 'expense')
            db.session.commit()
        return expense

    @staticmethod
    def delete_expense(expense_id, user_id):
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_expenses(user_id, filters=None):
        query = Expense.query.filter_by(user_id=user_id)
        
        if filters:
            if 'category_id' in filters and filters['category_id']:
                query = query.filter_by(category_id=filters['category_id'])
            if 'payment_method' in filters and filters['payment_method']:
                query = query.filter_by(payment_method=filters['payment_method'])
            if 'type' in filters and filters['type']:
                query = query.filter_by(type=filters['type'])
            
        expenses = query.all()
        return merge_sort_expenses(expenses, key='date', reverse=True)

    @staticmethod
    def get_expense_by_id(expense_id, user_id):
        return Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    @staticmethod
    def get_summary_stats(user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        
        total_income = sum(e.amount for e in expenses if e.type == 'income')
        total_expense = sum(e.amount for e in expenses if e.type == 'expense')
        balance = total_income - total_expense
        
        # Top spending category (only expenses)
        expense_only = [e for e in expenses if e.type == 'expense']
        category_totals = aggregate_by_category(expense_only)
        
        highest_category = None
        max_amount = 0
        for cat, amount in category_totals.items():
            if amount > max_amount:
                max_amount = amount
                highest_category = cat
                
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'highest_category': highest_category,
            'highest_amount': max_amount
        }

    @staticmethod
    def get_analysis_data(user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        
        # 1. Daily Activity (Bar Chart)
        daily_data = {}
        for e in expenses:
            date_str = e.date.strftime('%Y-%m-%d')
            if date_str not in daily_data:
                daily_data[date_str] = {'income': 0, 'expense': 0}
            daily_data[date_str][e.type] += e.amount
            
        sorted_dates = sorted(daily_data.keys())
        daily_chart_data = {
            'dates': sorted_dates,
            'income': [daily_data[d]['income'] for d in sorted_dates],
            'expense': [daily_data[d]['expense'] for d in sorted_dates]
        }

        # 2. Monthly Expenses (Pie Chart & Top Categories)
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_expenses = [e for e in expenses if e.type == 'expense' and e.date.month == current_month and e.date.year == current_year]
        
        category_data = aggregate_by_category(monthly_expenses)
        sorted_categories = dict(sorted(category_data.items(), key=lambda item: item[1], reverse=True))
        
        # 3. Prefix Sum (Cumulative Spending)
        # Filter expenses for current month for prefix sum as well, or use all time? 
        # Let's use current month for consistency with the analysis page context usually
        prefix_sum_data = compute_daily_prefix_sum(monthly_expenses)

        return {
            'daily_activity': daily_chart_data,
            'monthly_breakdown': sorted_categories, # For Chart.js
            'category_breakdown': sorted_categories, # For Template Loop (Fixing UndefinedError)
            'prefix_sum': prefix_sum_data # For Template Table
        }
    
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def export_expenses(user_id, start_date, end_date):
        # Validate date range
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if (end - start).days > 30:
            raise ValueError("Date range cannot exceed 30 days.")
            
        expenses = Expense.query.filter(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end).all()
        
        data = []
        for e in expenses:
            data.append({
                'Date': e.date.strftime('%Y-%m-%d'),
                'Type': e.type.title(),
                'Category': e.category.name if e.category else 'Uncategorized',
                'Amount': e.amount,
                'Payment Method': e.payment_method,
                'Note': e.note
            })
            
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Expenses')
            
        output.seek(0)
        return output
