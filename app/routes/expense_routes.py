from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_required, current_user
from app.services.expense_service import ExpenseService
from app.models import Category

expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/expenses')
@login_required
def list_expenses():
    filters = {
        'category_id': request.args.get('category_id'),
        'payment_method': request.args.get('payment_method'),
        'type': request.args.get('type')
    }
    expenses = ExpenseService.get_expenses(current_user.id, filters)
    categories = Category.query.all()
    return render_template('expense/list.html', expenses=expenses, categories=categories)

@expense_bp.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        ExpenseService.create_expense(request.form, current_user.id)
        flash('Expense added successfully!')
        return redirect(url_for('expense.list_expenses'))
        
    categories = Category.query.all()
    return render_template('expense/form.html', categories=categories, action='Add')

@expense_bp.route('/expenses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = ExpenseService.get_expense_by_id(id, current_user.id)
    if not expense:
        flash('Expense not found')
        return redirect(url_for('expense.list_expenses'))
        
    if request.method == 'POST':
        ExpenseService.update_expense(id, request.form, current_user.id)
        flash('Expense updated successfully!')
        return redirect(url_for('expense.list_expenses'))
        
    categories = Category.query.all()
    return render_template('expense/form.html', categories=categories, expense=expense, action='Edit')

@expense_bp.route('/expenses/<int:id>/delete')
@login_required
def delete_expense(id):
    if ExpenseService.delete_expense(id, current_user.id):
        flash('Expense deleted successfully!')
    else:
        flash('Error deleting expense')
    return redirect(url_for('expense.list_expenses'))

@expense_bp.route('/expenses/export', methods=['POST'])
@login_required
def export_expenses():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    try:
        output = ExpenseService.export_expenses(current_user.id, start_date, end_date)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'expenses_{start_date}_to_{end_date}.xlsx'
        )
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('dashboard.analysis'))
    except Exception as e:
        flash('An error occurred during export.', 'error')
        return redirect(url_for('dashboard.analysis'))
