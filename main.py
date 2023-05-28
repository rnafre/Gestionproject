import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database
from Etudiant import Etudiant

root = tk.Tk()
root.title("Gestion Notes")
root.geometry("400x300")
root.configure(background="#F4F4F4")

db = Database('notes.db')

# Styling
style = ttk.Style()
style.configure("TButton", background="#FF6B6B", foreground="#4949c6")
style.configure("TLabel", background="#F4F4F4", foreground="#4949c6")
style.configure("TEntry", background="#FFFFFF", fieldbackground="#4949c6")
style.configure("TText", background="#FFFFFF", foreground="#4949c6")


def switch_to_input_form():
    display_frame.pack_forget()
    input_frame.pack()

def ajouter_personne():
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    matiere = matiere_entry.get()
    note = note_entry.get()
    date = date_entry.get()

    if nom and prenom and matiere and note and date:
        try:
            note = float(note)  # Make sure note is a valid float
        except ValueError:
            messagebox.showerror("Invalid note", "Please enter a valid float for note.")
            return
        db.ajouter_noteEtudiant(nom, prenom, matiere, note,date)
        result_label.configure(
            text="Les informations ont été sauvegardées avec succès dans la base de données 'notes.db'.")
        clear_input_fields()
        switch_to_display_form()  # Refresh the display table
    else:
        result_label.configure(text="Veuillez remplir tous les champs.", foreground="red")


def clear_input_fields():
    nom_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    matiere_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


# Display Form Interface
def switch_to_display_form():
    input_frame.pack_forget()
    display_frame.pack()
    afficher_notesEtudiant()


def afficher_notesEtudiant():
    etudiants = db.recuperer_etudiants()

    for row in table.get_children():
        table.delete(row)

    for etudiant in etudiants:
        table.insert("", "end", values=(etudiant.nomEtudiant, etudiant.prenomEtudiant,etudiant.matiere, etudiant.note, etudiant.date))

    result_label.configure(
        text="Les informations ont été récupérées avec succès depuis la base de données 'notes.db'.")


# Input Form
input_frame = tk.Frame(root, bg="#F4F4F4")
input_label = ttk.Label(input_frame, text="Nouveau etudiant", font=("Helvetica", 16), background="#F4F4F4")
result_label = ttk.Label(input_frame, text="", background="#F4F4F4")

nom_label = ttk.Label(input_frame, text="Nom:", background="#F4F4F4")
nom_entry = ttk.Entry(input_frame)

prenom_label = ttk.Label(input_frame, text="Prénom:", background="#F4F4F4")
prenom_entry = ttk.Entry(input_frame)

matiere_label = ttk.Label(input_frame, text="Matiere:", background="#F4F4F4")
matiere_entry = ttk.Entry(input_frame)

note_label = ttk.Label(input_frame, text="Note:", background="#F4F4F4")
note_entry = ttk.Entry(input_frame)

date_label = ttk.Label(input_frame, text="Date:", background="#F4F4F4")
date_entry = ttk.Entry(input_frame)

ajouter_button = ttk.Button(input_frame, text="Ajouter", command=ajouter_personne)
switch_to_display_button = ttk.Button(input_frame, text="Afficher", command=switch_to_display_form)

# Use grid to position widgets in horizontal layout
input_label.grid(row=0, column=0, columnspan=4, pady=5)
result_label.grid(row=1, column=0, columnspan=4)

nom_label.grid(row=2, column=0)
nom_entry.grid(row=2, column=1)

prenom_label.grid(row=2, column=2)
prenom_entry.grid(row=2, column=3)

matiere_label.grid(row=3, column=0)
matiere_entry.grid(row=3, column=1)

note_label.grid(row=3, column=2)
note_entry.grid(row=3, column=3)

date_label.grid(row=4, column=0)
date_entry.grid(row=4, column=1)

ajouter_button.grid(row=5, column=0, columnspan=2, pady=10)
switch_to_display_button.grid(row=5, column=2, columnspan=2)

# Display Form
display_frame = tk.Frame(root, bg="#F4F4F4")

display_label = ttk.Label(display_frame, text="Notes etudiants enregistrées", font=("Helvetica", 16), background="#F4F4F4")
display_label.pack(pady=10)

table_frame = ttk.Frame(display_frame)
table = ttk.Treeview(table_frame, columns=( "Nom", "Prénom", "Matiere", "Note","Date"), show="headings")

table.heading("Nom", text="Nom")
table.heading("Prénom", text="Prénom")
table.heading("Matiere", text="Matiere")
table.heading("Note", text="Note")
table.heading("Date", text="Date")


table.column("Nom", width=150)
table.column("Prénom", width=150)
table.column("Matiere", width=80)
table.column("Note", width=150)
table.column("Date", width=150)

table.tag_configure("oddrow", background="#E8E8E8")
table.tag_configure("evenrow", background="#FFFFFF")

table.pack(padx=10, pady=10)
table_frame.pack(padx=10, pady=5)

switch_to_input_button = ttk.Button(display_frame, text="Retour", command=switch_to_input_form)
switch_to_input_button.pack(pady=7)


# Other Functions
def on_quit():
    db.fermer_connexion()
    root.destroy()


# Quit Button
quit_button = ttk.Button(root, text="Fermer", command=on_quit)
quit_button.pack(pady=10)

# Start the program
switch_to_input_form()
root.mainloop()

print("Fin du programme.")
