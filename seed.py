from app import create_app, db
from app.models import Category

def seed_categories():
    app = create_app()
    with app.app_context():
        # Check if categories exist
        if Category.query.first():
            print("Categories already exist.")
            return

        categories = [
            'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
            'Health & Fitness', 'Bills & Utilities', 'Education', 'Travel',
            'Salary', 'Freelance', 'Investment', 'Gifts', 'Other'
        ]

        for name in categories:
            db.session.add(Category(name=name))
        
        db.session.commit()
        print(f"Seeded {len(categories)} categories.")

if __name__ == '__main__':
    seed_categories()
