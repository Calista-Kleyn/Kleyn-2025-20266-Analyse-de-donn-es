#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

#Question 1 : 
# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    contenu = pd.read_csv(fichier)

# Mettre dans un commentaire le numéro de la question
# Question 1
# ...
#Question 2,3,4 fait
#Question 5 : Affichage du DataFarme complet
print(contenu)
#Question 6 : Nombre de lignes et de colonnes
nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)
print(f"\nNombre de lignes : {nb_lignes}")
print(f"Nombre de colonnes : {nb_colonnes}")
#Question 7 : Type de chaque colonne
print("\n--- Types de variables ---")
types_colonnes = contenu.dtypes
print(types_colonnes)
#Question 8 :Affichage des noms de colonnes
print("\n--- Noms des colonnes ---")
print(contenu.head(0))
#Question 9 : Séléction des nombres des inscrits
if 'Inscrits' in contenu.columns:
    inscrits = contenu['Inscrits']
else:
    inscrits = None
    print("⚠️ Colonne 'Inscrits' introuvable.")
#Question 10 : Calcul de la somme de chaque colonne numérique
print("\n--- Somme des colonnes numériques ---")
colonnes_numeriques = contenu.select_dtypes(include=['int64', 'float64']).columns
sommes = {}
for col in colonnes_numeriques:
    sommes[col] = contenu[col].sum()
    print(f"{col} : {sommes[col]}")
#Question 11 : Diagrammes en barres : nombre d’inscrits et votants par département
if 'Code département' in contenu.columns and 'Votants' in contenu.columns:
    for dep in contenu['Code département'].unique():
        data_dep = contenu[contenu['Code département'] == dep]
        valeurs = [data_dep['Inscrits'].sum(), data_dep['Votants'].sum()]
        labels = ['Inscrits', 'Votants']
        plt.bar(labels, valeurs)
        plt.title(f"Inscrits et votants - Département {dep}")
        plt.ylabel("Nombre d'électeurs")
        plt.savefig(f"images/bar_{dep}.png")
        plt.close()
#Question 12 : Diagrammes circulaires : votes blancs, nuls, abstention par département
colonnes_circulaires = ['Blancs', 'Nuls', 'Abstentions']
if all(c in contenu.columns for c in colonnes_circulaires):
    for dep in contenu['Code département'].unique():
        data_dep = contenu[contenu['Code département'] == dep]
        valeurs = [data_dep[c].sum() for c in colonnes_circulaires]
        plt.pie(valeurs, labels=colonnes_circulaires, autopct='%1.1f%%')
        plt.title(f"Répartition votes blancs/nuls/abstention - {dep}")
        plt.savefig(f"images/pie_{dep}.png")
        plt.close()
#Question 13 : Histogramme de la distribution des inscrits
if 'Inscrits' in contenu.columns:
    plt.hist(contenu['Inscrits'], bins=20)
    plt.title("Distribution des inscrits")
    plt.xlabel("Nombre d'inscrits")
    plt.ylabel("Fréquence")
    plt.savefig("images/histogramme_inscrits.png")
    plt.close()
print("\n✅ Traitement terminé ! Les graphiques sont enregistrés dans le dossier 'images'.")
#Bonus : 
# On suppose que les colonnes des candidats contiennent leur nom ou prénom
# Exemple : 'MACRON Emmanuel', 'LE PEN Marine', etc.
# On les détecte automatiquement :
colonnes_candidats = [
    c for c in contenu.columns
    if any(prenom in c.upper() for prenom in
           ["MACRON", "LE PEN", "MÉLENCHON", "ZEMMOUR", "PÉCRESSE",
            "JADOT", "HIDALGO", "DUPONT-AIGNAN", "LASSALLE", "POUTOU",
            "ARTHAUD", "ROUSSEL"] )
]

if len(colonnes_candidats) > 0:
    print("\n--- Colonnes candidates détectées ---")
    for c in colonnes_candidats:
        print(f" - {c}")

    # Dossier pour les graphiques bonus
    os.makedirs("images/bonus", exist_ok=True)

    # Diagrammes circulaires pour chaque département
    for dep in contenu['Code département'].unique():
        data_dep = contenu[contenu['Code département'] == dep]
        voix = [data_dep[c].sum() for c in colonnes_candidats]
        plt.pie(voix, labels=colonnes_candidats, autopct='%1.1f%%', startangle=90)
        plt.title(f"Résultats par candidat - Département {dep}")
        plt.savefig(f"images/bonus/pie_candidats_{dep}.png")
        plt.close()

    # Diagramme circulaire global pour la France entière
    voix_total = [contenu[c].sum() for c in colonnes_candidats]
    plt.pie(voix_total, labels=colonnes_candidats, autopct='%1.1f%%', startangle=90)
    plt.title("Résultats nationaux - 1er tour 2022")
    plt.savefig("images/bonus/pie_candidats_France.png")
    plt.close()

else:
    print("\n⚠️ Aucune colonne de candidats détectée automatiquement. Vérifie les noms de colonnes dans le CSV.")

print("\n✅ Toutes les analyses et graphiques ont été générés avec succès !")
print("📁 Les fichiers sont disponibles dans le dossier 'images/' et 'images/bonus/'.")