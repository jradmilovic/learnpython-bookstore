# LearnPython Book Store Web Aplikacija

LearnPython Book Store je web aplikacija razvijena koristeći Flask framework. 
Aplikacija omogućuje korisnicima pregledavanje, dodavanje u košaricu i kupovinu knjiga sa 
tematikom Python programskog jezika.

## Funkcionalnosti

- Registracija i prijava korisnika
- Pregledavanje kataloga knjiga
- Sortiranje knjiga po cijeni
- Dodavanje knjiga u košaricu
- Kupovina
- Admin panel za upravljanje korisnicima i bazom knjiga
- Odjava korisnika

## Postavljanje Projekta

1. **Kloniranje repozitorija:**
   ```
   git clone https://github.com/jradmilovic/learnpython-bookstore.git
   cd learnpython-bookstore
   ```
2. **Postavljanje virtualnog okruženja i instalacija potrebnih paketa:**
   ```
   python -m venv venv
   source venv/bin/activate  # Na Windowsu koristite `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Pokretanje aplikacije:**
   ```
   flask run
   ```
   Aplikacija će biti dostupna na http://127.0.0.1:5000/.

## Testni korisnici u bazi

Aplikaciju je moguće testirati koristeći sljedeće testne korisnike:
- Admin korisnik:
  - **Korisničko ime:** admin@admin.com
  - **Lozinka:** admin
- Obični korisnik:
  - **Korisničko ime:** jasmina@algebra.hr
  - **Lozinka:** jasmina

Moguće je kreirati i nove korisnike.

## Autor
- Jasmina Radmilović