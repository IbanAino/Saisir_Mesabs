# coding: utf-8
 
#https://www.pythontutorial.net/tkinter/tkinter-mvc/
#https://www.pythontutorial.net/tkinter/tkinter-validation/

#https://stackoverflow.com/questions/54421171/interactively-validating-entry-widget-content-in-tkinter-part-2-change-the-pr

#https://s15847115.domainepardefaut.fr/python/tkinter/fenetre_disposition_pack.html

#https://www.delftstack.com/howto/python/python-float-to-string/

#https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch06s07.html

"""
Iban FERNANDEZ, 2022, hivernage à Dumont d'Urville, TA72
Script pour la saisie des données absolues magnétiques
Ce scritp est un formulaire qui génère un fichier texte contenant les données au bon format.
Ce script se base sur l'architecture logicielle Modèle-Vue-Controller (MVC)

Modules :
tkinter : affichage graphique
configparser : lire des fichiers de configuration
re : utiliser les expressions régulières
datetime : définir la date du jour
math : calculer l'arrondi de valeurs d'angles
"""

from Model import *
from View import *
from Controller import *


##
# class App
#
# Cette classe est la classe principale du programme d'où sont instanciés le Modèle, la Vue et le Controlleur.
# De plus cette class lance la première étape de l'application, à savoir la lecture du fichier de configuraiton.
# En effet cette étape doit être réalisée une fois toutes les classes instanciées.
##
class App(tk.Tk):
    def __init__(self):

        pinguin = """
        OUTIL DE SAISIE DES DONNEES ABSOLUES

                    ~~~~~~
                  /'    -s- ~~~~      I <3 EOST and magnetism !
                 /'dHHb      ~~~~
                /'dHHHA     :
               /' VHHHHaadHHb:
              /'   `VHHHHHHHHb:
             /'      `VHHHHHHH:
            /'        dHHHHHHH:
            |        dHHHHHHHH:
            |       dHHHHHHHH:
            |       VHHHHHHHHH:
            |   b    HHHHHHHHV:
            |   Hb   HHHHHHHV'
            |   HH  dHHHHHHV'
            |   VHbdHHHHHHV'
            |    VHHHHHHHV'
            \    VHHHHHHH:
                \oodboooooodH
        HHHHHHHHHHHHHHHHHHHHHHHHGGN94

        Auteur : Iban FERNANDEZ
        Date : 2022
        """
        
        print(pinguin)

        super().__init__()

        self.title('Saisie de mesure absolue')

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view and model
        view.set_Controller(controller)
        model.set_Controller(controller)

        controller.load_Station_Config()


if __name__ == '__main__':
    app = App()
    app.mainloop()