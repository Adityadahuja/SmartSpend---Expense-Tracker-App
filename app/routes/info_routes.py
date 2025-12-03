from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import ContactMessage

info_bp = Blueprint('info', __name__)

@info_bp.route('/about')
def about():
    return render_template('info/about.html')

@info_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
        else:
            new_message = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('info.contact'))
            
    return render_template('info/contact.html')
