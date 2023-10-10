from flask_admin.contrib.sqla import ModelView
import flask_login as login
from pybookstore.models import User
class AdminView(ModelView):
  """
  Prilagođeni pogled modela za administrativno sučelje koje nasljeđuje od Flask-Admin ModelView.
  Ovaj pogled omogućuje dodatnu kontrolu pristupa tako da samo administratori mogu pristupiti
  administrativnom sučelju.
  """
  def is_accessible(self):
    """
     Provjerava je li trenutno prijavljeni korisnik administrator,
     kako bi se omogućio ili onemogućio pristup administrativnom sučelju.

     Returns:
         bool: True ako je trenutno prijavljeni korisnik administrator, inače False.
     """
    if login.current_user.is_authenticated:
      if login.current_user.get_id():
        user = User.query.get(login.current_user.get_id())
        return user.is_admin
    return False