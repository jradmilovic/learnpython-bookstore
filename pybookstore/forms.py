from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired, NumberRange
from pybookstore.models import User
from datetime import date


class RegistrationForm(FlaskForm):
    """
    Forma za registraciju korisnika
    """
    username = StringField('Korisničko ime',
                           validators=[DataRequired('Molimo unesite korisničko ime'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired(), Regexp('^.{5,10}$',
                                                                           message='Lozinka treba sadržavati između 5 i 10 znakova.')])
    confirm_password = PasswordField('Potvrdi lozinku',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Lozinke se moraju poklapati')])
    submit = SubmitField('Registriraj se')

    def validate_username(self, username):
        """
        Validacija korisničkog imena
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Korisničko ime već postoji. Molimo odaberite drugo korisničko ime.')

    def validate_email(self, email):
        """
        Validacija email adrese
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email već postoji. Molimo registrirajte se s drugom email adresom.')


class LoginForm(FlaskForm):
    """
    Forma za prijavu korisnika
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    submit = SubmitField('Prijavi se')


class CheckoutForm(FlaskForm):
    """
    Forma za kupnju knjiga iz košarice
    """
    name = StringField("Ime i prezime", validators=[InputRequired('Molimo unesite Vaše ime'),
                                                    Length(min=0, max=30,
                                                           message="Unos mora biti manji od 30 znakova")])
    address = StringField("Adresa", validators=[InputRequired('Molimo unesite adresu'),
                                                Length(min=0, max=30, message="Unos mora biti manji od 30 znakova")])
    city = StringField("Grad/Mjesto", validators=[InputRequired('Molimo unesite grad/mjesto'),
                                                  Length(min=0, max=30, message="Unos mora biti manji od 30 znakova")])
    postcode = StringField("Poštanski broj", validators=[InputRequired('Molimo unesite poštanski broj')])
    cardnumber = IntegerField("Broj kreditne kartice",
                              validators=[InputRequired('Molimo unesite broj kreditne kartice'),
                                          NumberRange(min=100000000000000, max=9999999999999999,
                                                      message="Broj kreditne kartice mora sadržavati 16 znamenki")])
    expiryyear = IntegerField("godina", validators=[InputRequired('Molimo unesite godinu važenja kartice'),
                                                    NumberRange(min=date.today().year, max=date.today().year + 100,
                                                                message="Mora biti trenutna ili kasnija godina")])
    expirymonth = SelectField("mjesec",
                              choices=[(1, "Siječanj"), (2, 'Veljača'), (3, 'Ožujak'), (4, 'Travanj'), (5, 'Svibanj'),
                                       (6, 'Lipanj'), (7, 'Srpanj'), (8, 'Kolovoz'), (9, 'Rujan'), (10, 'Listopad'),
                                       (11, 'Studeni'), (12, 'Prosinac')], coerce=int)
    cvv = IntegerField("CVV", validators=[InputRequired('Molimo unesite CVV broj'),
                                          NumberRange(min=100, max=9999,
                                                      message="CVV broj mora sadržavati 3 ili 4 znamenke")])
    submit = SubmitField('Potvrdi kupnju', validators=[InputRequired()])

    def validate_expirymonth(self, expirymonth):
        """
        Validacija broja kreditne kartice
        """
        if self.expiryyear.data == date.today().year:
            if expirymonth.data < date.today().month:
                raise ValidationError('Molimo unesite ispravan datum.')
