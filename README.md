# Outil de saisie des mesures absolues

**Auteur :** Iban FERNANDEZ

**Date :** 2022

Cet outil est dédié à l'opérateur qui saisi les masabs à l'ordinateur et est optimisé spécialement pour cette tâche.

## Installation

Tous les fichiers suivants doivent être copiés ensembles dans un même répertoire :
- Saisir.py
- Model.py
- View.py
- Controller.py
- config.txt
- README.md

Modules Python3 supplémentaires à télécharger :
- **tkinter** : affichage graphique
- **configparser** : lire des fichiers de configuration
- **re** : utiliser les expressions régulières
- **datetime** : définir la date du jour

```bash:
sudo apt-get install python3-tk
pip install configparser
pip install regex
pip install datetime
```

## Utilisation

La fonction principale de l'outil est de saisir les mesabs. La touche TAB permet de passer d'un champ d'entrée à l'autre sans sourie. Une vérification des entrées utilisateur vérifie les données. En cas de valeur erronée le champ se colore en rouge.

Cet outil permet également d'ouvrir une ancienne masabs pour la modifier.