from app import create_app, db
from app.models import Expense, Category

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Expense': Expense, 'Category': Category}

if __name__ == '__main__':
    app.run(debug=True)
