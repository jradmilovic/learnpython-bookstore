from pybookstore import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Book(db.Model):
    """
    Klasa za modeliranje knjiga u bazi podataka
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')


class User(UserMixin, db.Model):
    """
    Klasa za modeliranje korisnika u bazi podataka
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        """
        Metoda za zaštitu čitanja lozinke.
        """
        raise AttributeError('lozinka se ne može čitati')

    @password.setter
    def password(self, password):
        """
        Metoda za postavljanje hashirane lozinke.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Metoda za provjeru istovjetnosti unesene lozinke sa hashiranom lozinkom
        """
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """
    Metoda za učitavanje korisnika iz baze podataka.
    """
    return User.query.get(int(user_id))
