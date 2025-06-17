import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fichier_excel = 'historique_predictions.xlsx'

# Charger les données CSV
df = pd.read_csv("eleves.csv")

X = df[['heures_etude', 'presence', 'moyenne', 'absences', 'sommeil', 'participation', 'stress']]
y = df['reussite']

# Entraîner le modèle
model = LogisticRegression()
model.fit(X, y)

fenetre = tk.Tk()
fenetre.title("Prédiction de la Réussite Scolaire")
fenetre.geometry("500x700")

champs = {
    'heures_etude': None,
    'presence': None,
    'moyenne': None,
    'absences': None,
    'sommeil': None,
    'participation': None,
    'stress': None
}

# Création des champs d'entrée
for champ in champs:
    label = tk.Label(fenetre, text=champ.replace("_", " ").capitalize() + " :")
    label.pack(pady=3)
    entry = tk.Entry(fenetre)
    entry.pack()
    champs[champ] = entry

def enregistrer_prediction(valeurs, resultat):
    colonnes = list(champs.keys()) + ['Resultat']
    nouvelle_ligne = dict(zip(champs.keys(), valeurs))
    nouvelle_ligne['Resultat'] = resultat

    if os.path.exists(fichier_excel):
        df = pd.read_excel(fichier_excel)
        df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    else:
        df = pd.DataFrame([nouvelle_ligne], columns=colonnes)

    df.to_excel(fichier_excel, index=False)

def exporter_excel():
    if os.path.exists(fichier_excel):
        messagebox.showinfo("Export Excel", f"L'historique est enregistré dans '{fichier_excel}'.")
    else:
        messagebox.showwarning("Export Excel", "Aucun historique à exporter pour l'instant.")

def predire():
    try:
        valeurs = []
        for champ, entry in champs.items():
            val = entry.get()
            if val.strip() == "":
                raise ValueError(f"Le champ {champ} est vide.")
            val_float = float(val)

            if champ == 'heures_etude' and val_float < 0:
                raise ValueError("Les heures d'étude ne peuvent pas être négatives.")
            if champ == 'stress' and not (0 <= val_float <= 10):
                raise ValueError("Le stress doit être entre 0 et 10.")
            valeurs.append(val_float)

        prediction = model.predict([valeurs])
        proba = model.predict_proba([valeurs])[0][1] * 100

        resultat = "REUSSITE" if prediction[0] == 1 else "ECHEC"

        # Création d'une nouvelle fenêtre résultat colorée
        fen_res = tk.Toplevel(fenetre)
        fen_res.title("Résultat de la Prédiction")
        fen_res.geometry("300x150")

        couleur = "#27ae60" if resultat == "REUSSITE" else "#c0392b"
        label = tk.Label(fen_res, text=f"Prédiction : {resultat}\nProbabilité : {proba:.2f}%", 
                         font=("Arial", 16), fg="white", bg=couleur)
        label.pack(expand=True, fill="both")

        enregistrer_prediction(valeurs, resultat)
    except ValueError as ve:
        messagebox.showerror("Erreur de saisie", str(ve))
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

def reinitialiser():
    for entry in champs.values():
        entry.delete(0, tk.END)

def afficher_historique():
    if not os.path.exists(fichier_excel):
        messagebox.showinfo("Info", "Aucun historique trouvé.")
        return

    fenetre_hist = tk.Toplevel(fenetre)
    fenetre_hist.title("Historique des Prédictions")
    fenetre_hist.geometry("700x400")

    texte = scrolledtext.ScrolledText(fenetre_hist, width=80, height=25)
    texte.pack()

    df_hist = pd.read_excel(fichier_excel)
    contenu = df_hist.to_string(index=False)
    texte.insert(tk.END, contenu)
    texte.config(state=tk.DISABLED)

def afficher_graphique():
    if not os.path.exists(fichier_excel):
        messagebox.showinfo("Info", "Aucun historique trouvé.")
        return

    df_hist = pd.read_excel(fichier_excel)

    counts = df_hist['Resultat'].value_counts()

    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(counts.index, counts.values, color=['green' if res == 'REUSSITE' else 'red' for res in counts.index])
    ax.set_title("Répartition des Prédictions")
    ax.set_ylabel("Nombre")
    ax.set_xlabel("Résultat")
    ax.grid(axis='y')

    fenetre_graph = tk.Toplevel(fenetre)
    fenetre_graph.title("Graphique des Prédictions")

    canvas = FigureCanvasTkAgg(fig, master=fenetre_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Boutons dans la fenêtre principale
btn_reset = tk.Button(fenetre, text="Réinitialiser", command=reinitialiser)
btn_reset.pack(pady=5)
btn_export = tk.Button(fenetre, text="Exporter Excel", command=exporter_excel)
btn_export.pack(pady=5)
tk.Button(fenetre, text="Prédire", command=predire, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(fenetre, text="Afficher Historique", command=afficher_historique, bg="#f39c12", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(fenetre, text="Afficher Graphique", command=afficher_graphique, bg="#27ae60", fg="white", font=("Arial", 12)).pack(pady=10)

fenetre.mainloop()
