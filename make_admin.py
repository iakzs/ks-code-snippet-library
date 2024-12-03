from app import create_app, db
from app.models import User
import sys

def make_admin(username):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user is None:
            print(f"Error: User '{username}' not found")
            return
        
        user.is_admin = True
        db.session.commit()
        print(f"Successfully made {username} an admin!")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    make_admin(username)