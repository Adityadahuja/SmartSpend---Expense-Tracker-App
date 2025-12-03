from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = AuthService.authenticate_user(email, password)
        if not user:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('dashboard.index'))
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        salary = request.form.get('salary', 0.0)
        
        try:
            salary = float(salary)
        except (ValueError, TypeError):
            salary = 0.0
        
        user = AuthService.register_user(name, email, password, salary)
        if not user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
            
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
