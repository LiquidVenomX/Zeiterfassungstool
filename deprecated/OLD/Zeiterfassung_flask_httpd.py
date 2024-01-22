import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimeschluessel'  # Geheimer Schlüssel für Sessions (kann beliebig geändert werden)
login_manager = LoginManager(app)

# Definition der Benutzerklasse, die das UserMixin von Flask-Login erweitert
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# Flask-Login-Funktion zum Laden des Benutzers anhand der Benutzer-ID
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

# Funktion zum Erstellen des Standardbenutzers (admin, 1234), wenn noch nicht vorhanden
def create_user():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', '1234'))
    conn.commit()
    conn.close()

# Initialisierung der Benutzertabelle in der Datenbank
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)''')
conn.commit()
conn.close()

# Überprüfen, ob der Standardbenutzer bereits vorhanden ist, andernfalls erstellen
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
existing_user = cursor.fetchone()
conn.close()

if not existing_user:
    create_user()

# Startpunkt der Anwendung: Anzeige des Login-Formulars
@app.route('/')
def index():
    return render_template('login.html')

# Route für den Login-Vorgang
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Datenbankverbindung und Überprüfung der Anmeldeinformationen
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Anmeldung erfolgreich: Benutzer in der Sitzung speichern und zum Dashboard weiterleiten
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            print(f"Benutzer {username} erfolgreich angemeldet!")
            return redirect(url_for('dashboard'))

        else:
            # Anmeldung fehlgeschlagen: Fehlermeldung ausgeben
            print("Falscher Benutzername oder Passwort!")

    return render_template('login.html')

# Geschützte Route für das Dashboard, nur zugänglich, wenn der Benutzer angemeldet ist
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route für die Abmeldung des Benutzers
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Startet die Flask-Anwendung, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    app.run(debug=True)
