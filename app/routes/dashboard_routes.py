from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.assistant_service import AssistantService
from app.services.expense_service import ExpenseService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    summary_stats = ExpenseService.get_summary_stats(current_user.id)
    analysis_data = ExpenseService.get_analysis_data(current_user.id)
    assistant_analysis = AssistantService.get_analysis(current_user)
    
    return render_template('dashboard/index.html', 
                         stats=summary_stats, 
                         data=analysis_data, 
                         assistant=assistant_analysis)

@dashboard_bp.route('/analysis')
@login_required
def analysis():
    analysis_data = ExpenseService.get_analysis_data(current_user.id)
    return render_template('dashboard/analysis.html', data=analysis_data)
