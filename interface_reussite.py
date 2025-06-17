import pandas as pd
import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import os

# Charger les données CSV
df = pd.read_csv("eleves.csv")

X = df[['heures_etude', 'presence', 'moyenne', 'absences', 'sommeil', 'participation', 'stress']]
y = df['reussite']

# Entraîner le modèle
model = LogisticRegression()
model.fit(X, y)

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Prédiction de la Réussite Scolaire")
fenetre.geometry("400x600")

champs = {
    'heures_etude': None,
    'presence': None,
    'moyenne': None,
    'absences': None,
    'sommeil': None,
    'participation': None,
    'stress': None
}

# Création des champs
for champ in champs:
    label = tk.Label(fenetre, text=champ.replace("_", " ").capitalize() + " :")
    label.pack(pady=3)
    entry = tk.Entry(fenetre)
    entry.pack()
    champs[champ] = entry

# Fonction d'enregistrement dans un fichier CSV
def enregistrer_prediction(valeurs, resultat):
    ligne = valeurs.copy()
    ligne.append(resultat)
    ligne.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    colonnes = list(champs.keys()) + ['prediction', 'timestamp']
    fichier = "historique_predictions.csv"

    if not os.path.exists(fichier):
        # Créer le fichier avec en-tête si pas encore là
        df_save = pd.DataFrame([ligne], columns=colonnes)
        df_save.to_csv(fichier, index=False)
    else:
        # Ajouter une ligne
        df_save = pd.DataFrame([ligne], columns=colonnes)
        df_save.to_csv(fichier, mode='a', header=False, index=False)

# Fonction de prédiction
def predire():
    try:
        valeurs = []
        for champ, entry in champs.items():
            valeurs.append(float(entry.get()))
        
        prediction = model.predict([valeurs])
        resultat = "REUSSITE" if prediction[0] == 1 else "ECHEC"

        # Afficher
        messagebox.showinfo("Résultat", f"Prédiction : {resultat}")

        # Enregistrer
        enregistrer_prediction(valeurs, resultat)

    except Exception as e:
        messagebox.showerror("Erreur", f"Veuillez entrer des valeurs valides.\n{e}")

# Bouton prédire
tk.Button(fenetre, text="Prédire", command=predire, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=20)

fenetre.mainloop()
