from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


# Kreiranje Flask app instance i konfiguracija
app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicijalizacija SQLAlchemy i LoginManager instance
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from pybookstore import routes
from pybookstore.views import AdminView
from pybookstore.models import User, Book

# Kreiranje Admin sučelja za upravljanje korisnicima i bazom knjiga
admin = Admin(app,name='Admin panel',template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Book, db.session))

# Kreiranje definiranih tablica u bazi
with app.app_context():
    db.create_all()