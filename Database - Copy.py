import sqlite3
from Etudiant import Etudiant


class Database:
    def __init__(self, db_name):
        self.connexion = sqlite3.connect(db_name)
        self.cursor = self.connexion.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS NotesEtudiant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nomEtudiant TEXT,
                prenomEtudiant TEXT,
                matiere TEXT,
                note FLOAT,
                date TEXT
            )
        ''')
        self.connexion.commit()

    def ajouter_noteEtudiant(self, nomEtudiant, prenomEtudiant, matiere, note,date):
        self.cursor.execute("""
                INSERT INTO NotesEtudiant (nomEtudiant, prenomEtudiant, matiere, note,date) VALUES (?, ?, ?, ?,?)
            """, (nomEtudiant, prenomEtudiant, matiere, note,date))
        self.connexion.commit()

    def recuperer_etudiants(self):
        self.cursor.execute('''
            SELECT * FROM NotesEtudiant
        ''')
        rows = self.cursor.fetchall()
        etudiants = []
        for row in rows:
            etudiant = Etudiant(*row)  # Constructing the Personne object
            etudiants.append(etudiant)
        return etudiants

    def fermer_connexion(self):
        self.connexion.close()
