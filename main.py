"""
Autore: [Luca Rulvoni]
Versione: [0.0.1]
Data: [15/07/2023]

Descrizione: [Un semplice programma scritto in python per gestire attività usando tkinter e sqplite e creazione file pdf]

[]
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas

# Connessione al database
conn = sqlite3.connect('attivita.db')
c = conn.cursor()

# Creazione della tabella se non esiste
c.execute('''CREATE TABLE IF NOT EXISTS attivita
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             attivita TEXT NOT NULL,
             descrizione TEXT NOT NULL,
             data_inizio TEXT NOT NULL,
             data_fine TEXT NOT NULL,
             svolta INTEGER NOT NULL)''')
conn.commit()


# Funzione per aggiungere una nuova attività
def aggiungi_attivita():
    attivita = attivita_entry.get()
    descrizione = descrizione_entry.get()
    data_inizio = data_inizio_entry.get()
    data_fine = data_fine_entry.get()
    svolta = svolta_entry.get()

    if attivita and descrizione and data_inizio and data_fine and svolta:
        c.execute("INSERT INTO attivita (attivita, descrizione, data_inizio, data_fine, svolta) VALUES (?, ?, ?, ?, ?)",
                  (attivita, descrizione, data_inizio, data_fine, svolta))
        conn.commit()
        messagebox.showinfo("Successo", "Attività aggiunta con successo!")
        pulisci_campi()
        visualizza_attivita()
    else:
        messagebox.showerror("Errore", "Si prega di compilare tutti i campi!")


# Funzione per eliminare un'attività
def elimina_attivita():
    id_attivita = id_entry.get()

    if id_attivita:
        c.execute("DELETE FROM attivita WHERE id=?", (id_attivita,))
        conn.commit()
        messagebox.showinfo("Successo", "Attività eliminata con successo!")
        pulisci_campi()
        visualizza_attivita()
    else:
        messagebox.showerror("Errore", "Si prega di inserire l'ID dell'attività da eliminare!")


# Funzione per creare il PDF
def crea_pdf():
    c.execute("SELECT * FROM attivita")
    result = c.fetchall()

    pdf = canvas.Canvas("attivita.pdf")
    pdf.setFont("Helvetica", 12)

    y = 750
    for row in result:
        attivita, descrizione, data_inizio, data_fine, svolta = row[1], row[2], row[3], row[4], row[5]
        text = f"Attività: {attivita}\nDescrizione: {descrizione}\nData inizio: {data_inizio}\nData fine: {data_fine}\nSvolta: {svolta}\n"
        pdf.drawString(50, y, text)
        y -= 100

    pdf.save()
    messagebox.showinfo("Successo", "PDF creato con successo!")


# Funzione per visualizzare le attività nel treeview
def visualizza_attivita():
    c.execute("SELECT * FROM attivita")
    result = c.fetchall()

    # Pulizia del treeview
    for row in attivita_treeview.get_children():
        attivita_treeview.delete(row)

    # Aggiunta delle attività al treeview
    for row in result:
        attivita_treeview.insert('', 'end', values=row[1:])


# Funzione per pulire i campi di input
def pulisci_campi():
    id_entry.delete(0, tk.END)
    attivita_entry.delete(0, tk.END)
    descrizione_entry.delete(0, tk.END)
    data_inizio_entry.delete(0, tk.END)
    data_fine_entry.delete(0, tk.END)
    svolta_entry.delete(0, tk.END)


# Creazione dell'interfaccia grafica con Tkinter
root = tk.Tk()
root.title("Gestione Attività")

# Frame per le operazioni di aggiunta ed eliminazione
frame_operazioni = tk.Frame(root)
frame_operazioni.pack(pady=10)

id_label = tk.Label(frame_operazioni, text="ID:")
id_label.grid(row=0, column=0, sticky="E")
id_entry = tk.Entry(frame_operazioni)
id_entry.grid(row=0, column=1, padx=10, pady=5)

attivita_label = tk.Label(frame_operazioni, text="Attività:")
attivita_label.grid(row=1, column=0, sticky="E")
attivita_entry = tk.Entry(frame_operazioni)
attivita_entry.grid(row=1, column=1, padx=10, pady=5)

descrizione_label = tk.Label(frame_operazioni, text="Descrizione:")
descrizione_label.grid(row=2, column=0, sticky="E")
descrizione_entry = tk.Entry(frame_operazioni)
descrizione_entry.grid(row=2, column=1, padx=10, pady=5)

data_inizio_label = tk.Label(frame_operazioni, text="Data inizio:")
data_inizio_label.grid(row=3, column=0, sticky="E")
data_inizio_entry = tk.Entry(frame_operazioni)
data_inizio_entry.grid(row=3, column=1, padx=10, pady=5)

data_fine_label = tk.Label(frame_operazioni, text="Data fine:")
data_fine_label.grid(row=4, column=0, sticky="E")
data_fine_entry = tk.Entry(frame_operazioni)
data_fine_entry.grid(row=4, column=1, padx=10, pady=5)

svolta_label = tk.Label(frame_operazioni, text="Svolta:")
svolta_label.grid(row=5, column=0, sticky="E")
svolta_entry = tk.Entry(frame_operazioni)
svolta_entry.grid(row=5, column=1, padx=10, pady=5)

aggiungi_button = tk.Button(frame_operazioni, text="Aggiungi", command=aggiungi_attivita)
aggiungi_button.grid(row=6, column=0, padx=10, pady=5)

elimina_button = tk.Button(frame_operazioni, text="Elimina", command=elimina_attivita)
elimina_button.grid(row=6, column=1, padx=10, pady=5)

crea_pdf_button = tk.Button(frame_operazioni, text="Crea PDF", command=crea_pdf)
crea_pdf_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Frame per visualizzare le attività
frame_visualizza = tk.Frame(root)
frame_visualizza.pack(pady=10)

attivita_treeview = ttk.Treeview(frame_visualizza, columns=(1, 2, 3, 4, 5), show="headings")
attivita_treeview.pack(side="left", padx=10)

attivita_treeview.heading(1, text="Attività")
attivita_treeview.heading(2, text="Descrizione")
attivita_treeview.heading(3, text="Data Inizio")
attivita_treeview.heading(4, text="Data Fine")
attivita_treeview.heading(5, text="Svolta")

attivita_treeview.column(1, width=100)
attivita_treeview.column(2, width=200)
attivita_treeview.column(3, width=100)
attivita_treeview.column(4, width=100)
attivita_treeview.column(5, width=50)

scrollbar = ttk.Scrollbar(frame_visualizza, orient="vertical", command=attivita_treeview.yview)
scrollbar.pack(side="right", fill="y")

attivita_treeview.configure(yscrollcommand=scrollbar.set)

visualizza_attivita()

root.mainloop()