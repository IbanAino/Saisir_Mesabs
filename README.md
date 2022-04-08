# Outil de saisie des mesures absolues

**Auteur :** Iban FERNANDEZ

**Date :** 2022

Cet outil est dédié à l'opérateur qui saisit les masabs à l'ordinateur et est optimisé spécialement pour cette tâche.

![Alt text](rsc_doc/graphical_interface.png?raw=true "Flower")

## Installation

Tous les fichiers doivent être copiés ensembles dans un même répertoire :
- Saisir.py
- Model.py
- View.py
- Controller.py
- config.txt
- README.md
- rsc_doc/*

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

Pour lancer le scrilogiciel, lancer le fichier Saisir.py avec Python3 (en se plaçant dans le répertoire du fichier):

```bash:
python3 Saisir.py
```

La fonction principale de l'outil est de saisir les mesabs. La touche TAB permet de passer d'un champ d'entrée à l'autre sans sourie. Une vérification des entrées utilisateur vérifie les données. En cas de valeur erronée le champ se colore en rouge.

Cet outil permet également d'ouvrir une ancienne masabs pour la modifier.

Les données pérènes telles que le nom de l'observatoire ou l'azimuth repère, qui ne sont pas vouées à être saisies par l'utilisateur, sont inscrites dans le fichier de config **config.txt**. Leur inaccessibilité dans l'interface graphique permet à l'utilisateur de son concentrer pleinement sur la saisie de la mesabs.