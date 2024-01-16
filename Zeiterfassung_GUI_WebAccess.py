import tkinter as tk
from tkinter import messagebox
import sqlite3

# Schritt 1: Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('zeit_erfassung.db')
cursor = conn.cursor()

# Schritt 2: Definiere die Hauptfenster-Variable "window"
window = tk.Tk()
window.title('Zeiterfassungstool')

# Schritt 3: Definiere Funktionen für Benutzerverwaltung
def benutzer_anlegen(benutzername, passwort):
    # Funktion zum Hinzufügen eines neuen Benutzers zur Datenbank
    cursor.execute('INSERT INTO benutzer (benutzername, passwort) VALUES (?, ?)', (benutzername, passwort))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Benutzer wurde erfolgreich angelegt!')

def benutzer_loeschen(benutzername):
    # Funktion zum Löschen eines Benutzers aus der Datenbank
    cursor.execute('DELETE FROM benutzer WHERE benutzername = ?', (benutzername,))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Benutzer wurde erfolgreich gelöscht!')

def passwort_aendern(benutzername, neues_passwort):
    # Funktion zum Ändern des Passworts eines Benutzers in der Datenbank
    cursor.execute('UPDATE benutzer SET passwort = ? WHERE benutzername = ?', (neues_passwort, benutzername))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Passwort wurde erfolgreich geändert!')

# Schritt 4: Definiere Funktionen für die GUI
def anmelden(benutzername, passwort):
    # Hier implementierst du die Anmeldefunktion
    # Zum Beispiel: Überprüfe die Anmeldeinformationen in der Datenbank
    # Wenn erfolgreich, zeige eine Erfolgsmeldung an, sonst zeige eine Fehlermeldung an
    if benutzername == 'admin' and passwort == '1234':
        messagebox.showinfo('Erfolg', 'Anmeldung erfolgreich!')
    else:
        messagebox.showerror('Fehler', 'Falscher Benutzername oder Passwort!')

def benutzer_anmelden_gui():
    anmelde_label = tk.Label(window, text='Benutzeranmeldung')
    anmelde_label.pack()

    benutzername_label = tk.Label(window, text='Benutzername:')
    benutzername_entry = tk.Entry(window)
    benutzername_label.pack()
    benutzername_entry.pack()

    passwort_label = tk.Label(window, text='Passwort:')
    passwort_entry = tk.Entry(window, show='*')
    passwort_label.pack()
    passwort_entry.pack()

    anmelden_button = tk.Button(window, text='Anmelden', command=lambda: anmelden(benutzername_entry.get(), passwort_entry.get()))
    anmelden_button.pack()

# Aufruf der Funktion für die Benutzeranmeldung GUI
benutzer_anmelden_gui()

# Schritt 5: Starte die Hauptfenster-Schleife
window.mainloop()
