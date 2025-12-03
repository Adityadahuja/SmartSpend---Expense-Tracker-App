from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Category, Expense
from datetime import datetime

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        salary = request.form.get('salary')
        log_transaction = request.form.get('log_transaction')
        
        try:
            salary = float(salary)
        except (ValueError, TypeError):
            flash('Invalid salary amount.')
            return redirect(url_for('settings.account'))
            
        current_user.salary = salary
        db.session.add(current_user)
        
        if log_transaction:
            salary_category = Category.query.filter_by(name='Salary').first()
            if not salary_category:
                salary_category = Category(name='Salary')
                db.session.add(salary_category)
                db.session.flush()
                
            expense = Expense(
                user_id=current_user.id,
                category_id=salary_category.id,
                amount=salary,
                date=datetime.utcnow(),
                payment_method='Bank Transfer',
                note='Salary Update',
                type='income'
            )
            db.session.add(expense)
            
        db.session.commit()
        flash('Account settings updated successfully.')
        return redirect(url_for('settings.account'))
        
    return render_template('settings/account.html')
