from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('expense')
    col_names = [c['name'] for c in columns]
    print(f"Columns found: {col_names}")
    if 'type' in col_names:
        print("SUCCESS: 'type' column exists!")
    else:
        print("FAILURE: 'type' column is MISSING!")
