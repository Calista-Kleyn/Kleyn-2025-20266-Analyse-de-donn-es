# Analyse des résultats du 1er tour de la présidentielle 2022

import pandas as pd
import matplotlib.pyplot as plt
import os


# Question 1 à 4 : Lecture du fichier CSV


# Chemin vers le fichier CSV
csv_path = "./data/resultats-elections-presidentielles-2022-1er-tour.csv"

# Lecture du fichier CSV avec pandas (dans un bloc with)
with open(csv_path, "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)


# Question 5 : Afficher le contenu

print("\n=== Question 5 : Aperçu du contenu ===")
print(contenu.head())


# Question 6 : Nombre de lignes et colonnes

print("\n=== Question 6 : Dimensions du tableau ===")
nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)
print(f"Nombre de lignes : {nb_lignes}")
print(f"Nombre de colonnes : {nb_colonnes}")


# Question 7 : Nature statistique des variables

print("\n=== Question 7 : Types de colonnes ===")
types_vars = {}
for col in contenu.columns:
    dtype = contenu[col].dtype
    if pd.api.types.is_integer_dtype(dtype):
        types_vars[col] = "int"
    elif pd.api.types.is_float_dtype(dtype):
        types_vars[col] = "float"
    elif pd.api.types.is_bool_dtype(dtype):
        types_vars[col] = "bool"
    else:
        types_vars[col] = "str"
    print(f"{col} : {types_vars[col]}")


# Question 8 : Afficher le nom des colonnes

print("\n=== Question 8 : Noms des colonnes ===")
print(contenu.columns)


# Question 9 : Sélection du nombre des inscrits

print("\n=== Question 9 : Colonne 'Inscrits' ===")

col_inscrits = [c for c in contenu.columns if "Inscrit" in c or "INSCRIT" in c or "inscrit" in c]
if col_inscrits:
    print(contenu[col_inscrits[0]].head())
else:
    print("Colonne 'Inscrits' non trouvée. Vérifie le nom exact dans le CSV.")
    print(contenu.columns)


# Question 10 : Calcul des effectifs 

print("\n=== Question 10 : Somme des colonnes numériques ===")
somme_colonnes = {}
for col, t in types_vars.items():
    if t in ["int", "float"]:
        somme_colonnes[col] = contenu[col].sum()
for col, val in somme_colonnes.items():
    print(f"{col} : {val}")


# Question 11 : Diagrammes en barres (Inscrits / Votants)

print("\n=== Question 11 : Diagrammes en barres ===")
os.makedirs("images/barres", exist_ok=True)

col_dept = [c for c in contenu.columns if "Département" in c or "departement" in c or "Libellé" in c]
col_votants = [c for c in contenu.columns if "Votant" in c or "votant" in c]

if col_dept and col_inscrits and col_votants:
    dept = col_dept[0]
    inscrits = col_inscrits[0]
    votants = col_votants[0]

    for i in range(len(contenu)):
        nom_dept = str(contenu[dept][i]).replace("/", "-")
        valeurs = [contenu[inscrits][i], contenu[votants][i]]
        plt.bar(["Inscrits", "Votants"], valeurs, color=["skyblue", "orange"])
        plt.title(f"{nom_dept} - Inscrits vs Votants")
        plt.ylabel("Nombre")
        plt.tight_layout()
        plt.savefig(f"images/barres/{nom_dept}.png")
        plt.close()
else:
    print("Impossible de créer les diagrammes : colonnes manquantes.")
    print(contenu.columns)


# Question 12 : Diagrammes circulaires 

print("\n=== Question 12 : Diagrammes circulaires ===")
os.makedirs("images/camemberts", exist_ok=True)

col_blancs = [c for c in contenu.columns if "Blanc" in c]
col_nuls = [c for c in contenu.columns if "Nul" in c]
col_exprimes = [c for c in contenu.columns if "Exprim" in c]
col_abst = [c for c in contenu.columns if "Abst" in c]

if col_dept and col_blancs and col_nuls and col_exprimes and col_abst:
    dept = col_dept[0]
    blancs, nuls, exprimes, abst = col_blancs[0], col_nuls[0], col_exprimes[0], col_abst[0]
    for i in range(len(contenu)):
        nom_dept = str(contenu[dept][i]).replace("/", "-")
        valeurs = [contenu[blancs][i], contenu[nuls][i], contenu[exprimes][i], contenu[abst][i]]
        labels = ["Blancs", "Nuls", "Exprimés", "Abstention"]
        plt.pie(valeurs, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title(f"{nom_dept} - Répartition des votes")
        plt.tight_layout()
        plt.savefig(f"images/camemberts/{nom_dept}.png")
        plt.close()
else:
    print("Impossible de créer les diagrammes circulaires : colonnes manquantes.")
    print(contenu.columns)

# Question 13 : Histogramme de la distribution des inscrits

print("\n=== Question 13 : Histogramme ===")
os.makedirs("images/histogrammes", exist_ok=True)

if col_inscrits:
    inscrits = col_inscrits[0]
    plt.hist(contenu[inscrits], bins=20, color="lightgreen", edgecolor="black")
    plt.title("Distribution des inscrits")
    plt.xlabel("Nombre d'inscrits")
    plt.ylabel("Fréquence")
    plt.tight_layout()
    plt.savefig("images/histogrammes/hist_inscrits.png")
    plt.close()
else:
    print("Colonne 'Inscrits' non trouvée.")
    print(contenu.columns)
# ----------------------------------------------------------
print("\n=== Fin du script ===")
print("Les graphiques sont enregistrés dans le dossier ./images/")

