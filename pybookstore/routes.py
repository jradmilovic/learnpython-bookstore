from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_user, logout_user
from pybookstore import app, db
from pybookstore.models import Book, User
from pybookstore.forms import RegistrationForm, LoginForm, CheckoutForm

@app.route("/")
@app.route("/home")
def home():
    """
    Ruta za prikazivanje početne stranice web trgovine. Prikazuje popis knjiga sortiran po cijeni.
    Korisnik može odabrati sortiranje po cijeni uzlazno ili silazno.

    Returns:
        render_template: Renderira 'shop.html' template s popisom knjiga i naslovom stranice.
    """
    id = request.args.get('id', default='1', type=int)
    if id == 1:
        books = Book.query.order_by(Book.price)
    else:
        books = Book.query.order_by(Book.price.desc())
    return render_template('shop.html', books=books, title=' LearnPython Book Store')

@app.route("/o-nama")
def about():
    """
    Ruta za prikazivanje stranice 'O nama'.

    Returns:
        render_template: Renderira 'o_nama.html' template s naslovom stranice.
    """
    return render_template('o_nama.html', title='O Nama')

@app.route("/admin")
def admin():
    """
    Ruta za prikazivanje admin panela.

    Returns:
        render_template: Renderira 'admin/index.html' template s naslovom stranice.
    """
    return render_template('admin/index.html', title='Admin Panel')

@app.route("/knjiga/<int:book_id>")
def book(book_id):
    """
    Ruta za prikazivanje detalja o odabranoj knjizi.

    Args:
        book_id (int): ID knjige koja se prikazuje.

    Returns:
        render_template: Renderira 'knjiga.html' template s detaljima o knjizi.
    """
    book = Book.query.get_or_404(book_id)

    return render_template('knjiga.html', book=book)


@app.route("/registracija", methods=['GET', 'POST'])
def register():
    """
    Ruta za registraciju novog korisnika. Ako je forma ispravno poslana,
    novi korisnik će biti kreiran i dodan u bazu podataka.

    Returns:
        render_template: Renderira 'registracija.html' template s formom za registraciju.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Vaš korisnički račun je kreiran. Možete se prijaviti.', 'success')
        return redirect(url_for('home'))

    return render_template('registracija.html', title='Registracija', form=form)

@app.route("/prijava", methods=['GET','POST'])
def login():
    """
    Ruta za prijavu postojećih korisnika. Ako su korisnički podaci ispravni,
    korisnik će biti prijavljen.

    Returns:
        render_template: Renderira 'prijava.html' template s formom za prijavu.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Uspješno ste prijavljeni')
            return redirect(url_for('home'))
        flash('Neispravno korisničko ime ili lozinka')

        return render_template('prijava.html', form=form)

    return render_template('prijava.html', title='Prijava', form=form)

@app.route("/odjava")
def logout():
    """
    Ruta za odjavu prijavljenih korisnika.

    Returns:
        redirect: Preusmjerava korisnika na početnu stranicu.
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/dodaj_u_kosaricu/<int:book_id>")
def add_to_cart(book_id):
    """
    Ruta za dodavanje knjige u korisničku košaricu.

    Args:
        book_id (int): ID knjige koja se dodaje u košaricu.

    Returns:
        redirect: Preusmjerava korisnika na stranicu košarice.
    """
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(book_id)

    flash("Knjiga je dodana u Vašu košaricu")
    return redirect("/kosarica")


@app.route("/kosarica", methods=['GET', 'POST'])
def cart_display():
    """
    Ruta za prikazivanje sadržaja korisničke košarice.

    Returns:
        render_template: Renderira 'kosarica.html' template s informacijama o artiklima u košarici.
    """
    if "cart" not in session:
        flash('Vaša košarica je prazna')
        return render_template("kosarica.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}
        total_price = 0
        total_quantity = 0
        for item in items:
            book = Book.query.get_or_404(item)
            total_price += book.price
            if book.id in cart:
                cart[book.id]["quantity"] += 1
            else:
                cart[book.id] = {"quantity":1, "title": book.title, "price":book.price}
            total_quantity = sum(item['quantity'] for item in cart.values())


        return render_template("kosarica.html", title='Vaša košarica', display_cart = cart, total = total_price, total_quantity = total_quantity)

@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
    """
    Ruta za uklanjanje knjige iz korisničke košarice.

    Args:
        book_id (int): ID knjige koja se uklanja iz košarice.

    Returns:
        redirect: Preusmjerava korisnika natrag na stranicu košarice.
    """
    if "cart" not in session:
        session["cart"] = []
    session["cart"].remove(book_id)
    flash("Knjiga je uklonjena iz Vaše košarice")
    session.modified = True
    return redirect("/kosarica")

@app.route("/kupovina", methods=['GET', 'POST'])
def checkout():
    """
    Ruta za procesiranje kupovine.

    Returns:
        render_template: Renderira 'kupovina.html' template s formom za unos podataka o kupnji.
    """
    if "cart" not in session:
        flash('Vaša košarica je prazna')
        return render_template("kosarica.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        total_price = 0
        for item in items:
            book = Book.query.get_or_404(item)
            total_price += book.price
        form = CheckoutForm()
        if form.validate_on_submit():
            return redirect(url_for('confirmation'))
        return render_template('kupovina.html', form=form, total=total_price)

@app.route("/potvrda", methods=['GET', 'POST'])
def confirmation():
    """
    Ruta za prikaz potvrde o uspješnoj kupnji.

    Returns:
        render_template: Renderira 'potvrda.html' template.
    """
    return render_template('potvrda.html')
