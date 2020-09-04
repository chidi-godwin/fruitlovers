from app import db, create_app
from app.models import User, Discount, Role, Product
import os

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Product=Product, Discount=Discount)
