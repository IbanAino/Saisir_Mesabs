from tkinter import Tk, W, E, messagebox
from tkinter import ttk
from tkinter.ttk import Frame, Button, Entry, Style
from tkinter import filedialog as fd
import tkinter as tk

from datetime import datetime

import re

import math

##
# class View
#
# Cette classe est la classe Vue de l'architecture logicielle Modèle - Vue - controlleur.
#
# Elle définie toute la partie interface graphique de l'application.
# L'interface graphique consite en une seule fenêtre contenant un formulaire à remplir.
# Elle se compose de cinq parties :
#
# - Entête, contenant des information sur la station stockées dans un fichier de configuraiton et la date.
#   Cette partie stocke ses données dans un dicionnaire propre.
#
# - Boutons "ENREGISTRER" et "charger une masabs", qui sont les deux fonctionnalitées de l'outil. Cette partie est un objet instancié.
#
# - Angles de visées de la cible. Cette partie est un formulaire de quatre champs. Cette partie est un objet instancié.
#   Cette partie stocke ses données dans un dicionnaire propre.
#
# - Mesures de X et de Y lors de l'ouverture et de la fermeture de la mesabs.
#   Cette partie contient quatre tableaux de champs d'entrées :
#    * ouverture X
#    * ouverture Y
#    * fermeture X
#    * fermeture Y
#   Chaque tableau est un onjet instacié à partir de la même classe
#   Cette partie stocke ses données dans un dicionnaire propre.
#
# - Etalonnages ouverture et fermeture
#   Cette partie contient quatre tableaux de champs d'entrées :
#    * étalonnage ouverture sonde en haut
#    * étalonnage ouverture sonde en bas
#    * étalonnage fermeture sonde en haut
#    * étalonnage fermeture sonde en bas
#   Chaque tableau est un onjet instacié à partir de la même classe
#   Cette partie stocke ses données dans un dicionnaire propre.
##

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.geometry("1200x920")
        parent.configure(bg = 'Light Grey')

        self.site = 'None'
        self.correction_F = 'None'
        self.rotation_Angle  = 'None'
        self.bearing_Azimuth = 'None'
        self.saving_Directory_Path = 'None'

        #------ TEXT ------
        Text_Frame(text = 'Mesures de X').place(x = 260, y = 220)
        Text_Frame(text = 'Mesures de Y').place(x = 840, y = 220)
        Text_Frame(text = 'Etalonnage ouverture').place(x = 520, y = 530)
        Text_Frame(text = 'Etalonnage fermeture').place(x = 520, y = 730)

        #------ BUTTONS ------
        self.buttons = Buttons_Frame(self.save_button_clicked, self.load_Button_Clicked)

        #------ ENTRIES ------
        self.entry_Header = Entry_Header()
        self.entry_Angles_From_Target = Entry_Angles_From_Target()
        # X and Y
        self.opening_Calibration_X = Entry_Table_X_Y()
        self.opening_Calibration_Y = Entry_Table_X_Y()
        self.closing_Calibration_X = Entry_Table_X_Y()
        self.closing_Calibration_Y = Entry_Table_X_Y()

        self.entry_Angles_From_Target.table_Opening_X = self.opening_Calibration_X
        self.entry_Angles_From_Target.table_Opening_Y = self.opening_Calibration_Y
        self.entry_Angles_From_Target.table_Closing_X = self.closing_Calibration_X
        self.entry_Angles_From_Target.table_Closing_Y = self.closing_Calibration_Y

        # Calibration
        self.calibration_Opening_Probe_Up = Entry_Table_Calibration(probe_Up = True)
        self.calibration_Opening_Probe_Down = Entry_Table_Calibration(probe_Up = False)
        self.calibration_Closing_Probe_Up = Entry_Table_Calibration(probe_Up = True)
        self.calibration_Closing_Probe_Down = Entry_Table_Calibration(probe_Up = False)
        
        self.buttons.place(x = 900, y = 40)

        self.entry_Header.place(x = 10, y = 40)
        self.entry_Angles_From_Target.place(x = 15, y = 140)

        self.opening_Calibration_X.place(x = 10, y = 250)
        self.opening_Calibration_Y.place(x = 610, y = 250)
        self.closing_Calibration_X.place(x = 10, y = 380)
        self.closing_Calibration_Y.place(x = 610, y = 380)
    
        self.calibration_Opening_Probe_Up.place(x = 10, y = 560)
        self.calibration_Opening_Probe_Down.place(x = 610, y = 560)
        self.calibration_Closing_Probe_Up.place(x = 10, y = 760)
        self.calibration_Closing_Probe_Down.place(x = 610, y = 760)

        # set the controller
        self.controller = None
      
    def set_Controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def save_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            self.controller.save_Data()
    
    def load_Button_Clicked(self):
        """
        Cette fonction active la lecture d'une saisie de mesure absolue lor du clic du bouton "charger une mesabs"
        """

        print("Load mesabs View")
        if self.controller:
                #self.controller.load_mesabs()
            self.select_file()


    def select_file(self):
        """
        Cette fonction permet de sélectionner un fichier de mesabs dans l'arborescence de fichiers de l'ordinateur.
        """
        filetypes = (
            ('mesabs from DRV', '*.drv'),
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir = self.saving_Directory_Path,
            filetypes=filetypes)
        
        if self.controller:
            self.controller.get_file_to_load(filename)



    def update_Station_Config(self):
        """
        Cette fonction remplis les champs du formulaire d'entrée avec les variables du programme.
        Cette fonction doit être appellée après que le programme ait définti ses variables en lisant le fichier de configuration.
        """
        self.entry_Header.text_station.configure(text = self.site)
        self.entry_Header.text_Correction_F_Measurement.configure(text = self.correction_F)
        self.entry_Header.text_Rotation_Angle.configure(text = self.rotation_Angle)
        self.entry_Header.text_Bearing_Azimuth.configure(text = self.bearing_Azimuth)

        self.entry_Angles_From_Target.bearing_Azimuth = self.bearing_Azimuth

    def show_Error_Message(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        print(message)
        messagebox.showerror('erreur', message)

    def show_Validation_Message(self, message):
        """
        Show a validation message
        :param message:
        :return:
        """
        print(message)
        messagebox.showinfo('information', message)

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.email_entry['foreground'] = 'black'
        self.email_var.set('')

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label['text'] = ''

    # Check user inputs
    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        self.email_entry['foreground'] = color

##
# class Entry_Table_X_Y
#
# Cette classe décrit un tableau de champs d'entrée pour saisir les mesures de X et Y.
# Cette classe est instanciée quatre fois dans l'interface graphique qui contient quatre de ces tableaux.
##
class Entry_Table_X_Y(tk.Frame):
    def __init__(self):
        super(Entry_Table_X_Y, self).__init__()
        self.configure(bg = 'Light Grey')

        # Validation commands
        self.validate_Command_Date = self.register(self.on_Validate_Date)
        self.validate_Command_Mang_Value = self.register(self.on_Validate_Magn_Value)

        # Labels
        ttk.Label(self, text='1', background = 'Light Grey').grid(row = 2, column = 1)
        ttk.Label(self, text='2', background = 'Light Grey').grid(row = 3, column = 1)
        ttk.Label(self, text='3', background = 'Light Grey').grid(row = 4, column = 1)
        ttk.Label(self, text='4', background = 'Light Grey').grid(row = 5, column = 1)
        ttk.Label(self, text='HH MM SS', background = 'Light Grey').grid(row = 1, column = 2)
        ttk.Label(self, text='angle', background = 'Light Grey').grid(row = 1, column = 3)
        ttk.Label(self, text='valeur', background = 'Light Grey').grid(row = 1, column = 4)

        # Times
        self.time_1_Var = tk.StringVar()
        self.time_2_Var = tk.StringVar()
        self.time_3_Var = tk.StringVar()
        self.time_4_Var = tk.StringVar()
        self.time_1_Entry = tk.Entry(self, validate="focusout", textvariable = self.time_1_Var, bg = 'white', fg = 'black')
        self.time_2_Entry = tk.Entry(self, validate="focusout", textvariable = self.time_2_Var, bg = 'white', fg = 'black')
        self.time_3_Entry = tk.Entry(self, validate="focusout", textvariable = self.time_3_Var, bg = 'white', fg = 'black')
        self.time_4_Entry = tk.Entry(self, validate="focusout", textvariable = self.time_4_Var, bg = 'white', fg = 'black')
        self.time_1_Entry.grid(row = 2, column = 2)
        self.time_2_Entry.grid(row = 3, column = 2)
        self.time_3_Entry.grid(row = 4, column = 2)
        self.time_4_Entry.grid(row = 5, column = 2)
        self.time_1_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_2_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_3_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_4_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))

        # Angles
        self.angle_1_Var = tk.StringVar(value = 0)
        self.angle_2_Var = tk.StringVar(value = 0)
        self.angle_3_Var = tk.StringVar(value = 0)
        self.angle_4_Var = tk.StringVar(value = 0)
        self.text_angle_1 = ttk.Label(self, width = 20, text = self.angle_1_Var.get())
        self.text_angle_2 = ttk.Label(self, width = 20, text = self.angle_2_Var.get())
        self.text_angle_3 = ttk.Label(self, width = 20, text = self.angle_3_Var.get())
        self.text_angle_4 = ttk.Label(self, width = 20, text = self.angle_4_Var.get())
        self.text_angle_1.config(anchor='center')
        self.text_angle_2.config(anchor='center')
        self.text_angle_3.config(anchor='center')
        self.text_angle_4.config(anchor='center')
        self.text_angle_1.grid(row = 2, column = 3)
        self.text_angle_2.grid(row = 3, column = 3)
        self.text_angle_3.grid(row = 4, column = 3) 
        self.text_angle_4.grid(row = 5, column = 3)
        self.text_angle_1.configure(background = "white")
        self.text_angle_2.configure(background = "white")
        self.text_angle_3.configure(background = "white")
        self.text_angle_4.configure(background = "white")
        self.text_angle_2.columnconfigure(0, weight = 1)

        # Magn value
        self.magn_Value_1_Var = tk.StringVar()
        self.magn_Value_2_Var = tk.StringVar()
        self.magn_Value_3_Var = tk.StringVar()
        self.magn_Value_4_Var = tk.StringVar()
        self.magn_Value_1_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_1_Var, bg = 'white', fg = 'black')
        self.magn_Value_2_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_2_Var, bg = 'white', fg = 'black')
        self.magn_Value_3_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_3_Var, bg = 'white', fg = 'black')
        self.magn_Value_4_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_4_Var, bg = 'white', fg = 'black')
        self.magn_Value_1_Entry.grid(row = 2, column = 4)
        self.magn_Value_2_Entry.grid(row = 3, column = 4)
        self.magn_Value_3_Entry.grid(row = 4, column = 4)
        self.magn_Value_4_Entry.grid(row = 5, column = 4)
        self.magn_Value_1_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_2_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_3_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_4_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))

    def on_Validate_Date(self, entry_name, new_value):
        """
        Cette fonction vérifie que l'heure entrée par l'utilisateur est bien formatée.
        Cette date doit être de la forme HHMMSS
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        print('OnValidateDate')
        print(entry_name)
        entry = self.nametowidget(entry_name)
        # Check the hours between 0 an 24, check the minutes between 0 and 59, check the seconds between 0 and 59 and chek the date lenght that should be 6 digits
        x = re.search("(?=^(2[0-3]|1[0-9]|0[0-9]))(?=^..[0-59])(?=^....[0-59])(?=[0-9]{6}$)", new_value)

        if x:
            print("Yes, there is at least one match!")
            entry.configure(background = '#98FB98')
        else:
            print("No match")
            entry.configure(background='#FFBCC1')
            return True

        return True

    def on_Validate_Magn_Value(self, entry_name, new_value):
        """
        Cette fonction vérifie que la valuer du magnétisme entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre -9999.9 et +9999.9
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        print('on_Validate_Magn_Value')
        entry = self.nametowidget(entry_name)
        entry.configure(background="#98FB98")

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Magn_Value(new_value))

            if (-9999.9 <= new_value and new_value <= 9999.9):
                entry.configure(background="#98FB98")

            else:
                entry.configure(background="#FFBCC1")

        except ValueError:
            entry.configure(background="#FFBCC1")
            return True

        return True

    def get_Data(self):
        """
        Cette fonction retoune un dicionnaire contenant toutes les données du tableau saisi par l'utilisteur.
        """
        self.dictionnary_Data_Values = {
            'time_1' : self.time_1_Entry.get(),
            'time_2' : self.time_2_Entry.get(),
            'time_3' : self.time_3_Entry.get(),
            'time_4' : self.time_4_Entry.get(),
            'angle_1' : self.text_angle_1.cget('text'),
            'angle_2' : self.text_angle_2.cget('text'),
            'angle_3' : self.text_angle_3.cget('text'),
            'angle_4' : self.text_angle_4.cget('text'),
            'magn_Value_1' : self.magn_Value_1_Entry.get(),
            'magn_Value_2' : self.magn_Value_2_Entry.get(),
            'magn_Value_3' : self.magn_Value_3_Entry.get(),
            'magn_Value_4' : self.magn_Value_4_Entry.get()
        }

        return(self.dictionnary_Data_Values)

    def update_Data(self, dictionnary_Data):
        """
        Cette fonction remplis automatiquement les champs d'entrées du firmulaire avec les données passées en paramètre.
        """
        self.time_1_Var.set(dictionnary_Data['time_1']),
        self.time_2_Var.set(dictionnary_Data['time_2']),
        self.time_3_Var.set(dictionnary_Data['time_3']),
        self.time_4_Var.set(dictionnary_Data['time_4']),
        self.text_angle_1.config(text = dictionnary_Data['angle_1']),
        self.text_angle_2.config(text = dictionnary_Data['angle_2']),
        self.text_angle_3.config(text = dictionnary_Data['angle_3']),
        self.text_angle_4.config(text = dictionnary_Data['angle_4']),
        self.magn_Value_1_Var.set(dictionnary_Data['magn_Value_1']),
        self.magn_Value_2_Var.set(dictionnary_Data['magn_Value_2']),
        self.magn_Value_3_Var.set(dictionnary_Data['magn_Value_3']),
        self.magn_Value_4_Var.set(dictionnary_Data['magn_Value_4'])

    def format_Magn_Value(self, value):
        """
        This function get a float and return a string with 1 digits after the comma, including the 0
        :return:
        """
        return(str(format(value, '.1f')))

##
# class Entry_Table_Calibration
#
# Cette classe décrit un tableau de champs d'entrée pour saisir les étalonnages ouverture et fermeture.
# Cette classe est instanciée quatre fois dans l'interface graphique qui contient quatre de ces tableaux.
##
class Entry_Table_Calibration(tk.Frame):
    def __init__(self, probe_Up):
        super(Entry_Table_Calibration, self).__init__()
        self.configure(bg = 'Light Grey')

        self.probe_Up = probe_Up

        # Validation commands
        self.validate_Command_Date = self.register(self.on_Validate_Date)
        self.validate_Command_Angle = self.register(self.on_Validate_Angle)
        self.validate_Command_Mang_Value = self.register(self.on_Validate_Magn_Value)
        self.validate_Command_Est_Magn = self.register(self.on_Validate_Est_Magn)
        

        # Labels
        ttk.Label(self, text='1', background = 'Light Grey').grid(row = 2, column = 1)
        ttk.Label(self, text='2', background = 'Light Grey').grid(row = 3, column = 1)
        ttk.Label(self, text='3', background = 'Light Grey').grid(row = 4, column = 1)
        ttk.Label(self, text='4', background = 'Light Grey').grid(row = 5, column = 1)
        ttk.Label(self, text='HH MM SS', background = 'Light Grey').grid(row = 1, column = 2)
        ttk.Label(self, text='angle', background = 'Light Grey').grid(row = 1, column = 3)
        ttk.Label(self, text='valeur', background = 'Light Grey').grid(row = 1, column = 4)

        if probe_Up is True:
            ttk.Label(self, text='sonde en haut Est magne', background = 'Light Grey').grid(row = 0, column = 1, columnspan = 2, padx=5, pady=5, sticky = tk.E)
        else:
            ttk.Label(self, text='sonde en bas Est magne', background = 'Light Grey').grid(row = 0, column = 1, columnspan = 2, padx=5, pady=5, sticky = tk.E)

        # Est magne
        self.est_Magn_Var = tk.StringVar()
        self.est_Magn_Entry = tk.Entry(self, validate = "focusout", textvariable = self.est_Magn_Var, bg = 'white', fg = 'black')
        self.est_Magn_Entry.grid(row = 0, column = 3)
        self.est_Magn_Entry.configure(validatecommand = (self.validate_Command_Est_Magn, "%W", "%P"))

        # Times
        self.time_1_Var = tk.StringVar()
        self.time_2_Var = tk.StringVar()
        self.time_3_Var = tk.StringVar()
        self.time_4_Var = tk.StringVar()
        self.time_1_Entry = tk.Entry(self, validate = "focusout", textvariable = self.time_1_Var, bg = 'white', fg = 'black')
        self.time_2_Entry = tk.Entry(self, validate = "focusout", textvariable = self.time_2_Var, bg = 'white', fg = 'black')
        self.time_3_Entry = tk.Entry(self, validate = "focusout", textvariable = self.time_3_Var, bg = 'white', fg = 'black')
        self.time_4_Entry = tk.Entry(self, validate = "focusout", textvariable = self.time_4_Var, bg = 'white', fg = 'black')
        self.time_1_Entry.grid(row = 2, column = 2)
        self.time_2_Entry.grid(row = 3, column = 2)
        self.time_3_Entry.grid(row = 4, column = 2)
        self.time_4_Entry.grid(row = 5, column = 2)
        self.time_1_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_2_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_3_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
        self.time_4_Entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))

        # Angles
        self.angle_1_Var = tk.StringVar()
        self.angle_2_Var = tk.StringVar(value = 0)
        self.angle_3_Var = tk.StringVar(value = 0)
        self.angle_4_Var = tk.StringVar(value = 0)
        self.angle_1_Entry = tk.Entry(self, validate="focusout", textvariable = self.angle_1_Var, bg = 'white', fg = 'black')
        self.angle_1_Entry.grid(row = 2, column = 3)
        self.angle_1_Entry.configure(validatecommand = (self.validate_Command_Angle, "%W", "%P"))
        self.text_angle_2 = ttk.Label(self, width = 20, text = self.angle_2_Var.get())
        self.text_angle_3 = ttk.Label(self, width = 20, text = self.angle_3_Var.get())
        self.text_angle_4 = ttk.Label(self, width = 20, text = self.angle_4_Var.get())
        self.text_angle_2.config(anchor = 'center')
        self.text_angle_3.config(anchor = 'center')
        self.text_angle_4.config(anchor = 'center')
        self.text_angle_2.grid(row = 3, column = 3)
        self.text_angle_3.grid(row = 4, column = 3) 
        self.text_angle_4.grid(row = 5, column = 3)
        self.text_angle_2.configure(background = "white")
        self.text_angle_3.configure(background = "white")
        self.text_angle_4.configure(background = "white")

        # Magn value
        self.magn_Value_1_Var = tk.StringVar(value = '0.0')
        self.magn_Value_2_Var = tk.StringVar()
        self.magn_Value_3_Var = tk.StringVar()
        self.magn_Value_4_Var = tk.StringVar()
        self.magn_Value_1_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_1_Var, bg = 'white', fg = 'black')
        self.magn_Value_2_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_2_Var, bg = 'white', fg = 'black')
        self.magn_Value_3_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_3_Var, bg = 'white', fg = 'black')
        self.magn_Value_4_Entry = tk.Entry(self, validate="focusout", textvariable = self.magn_Value_4_Var, bg = 'white', fg = 'black')
        self.magn_Value_1_Entry.grid(row = 2, column = 4)
        self.magn_Value_2_Entry.grid(row = 3, column = 4)
        self.magn_Value_3_Entry.grid(row = 4, column = 4)
        self.magn_Value_4_Entry.grid(row = 5, column = 4)
        self.magn_Value_1_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_2_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_3_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))
        self.magn_Value_4_Entry.configure(validatecommand = (self.validate_Command_Mang_Value, "%W", "%P"))

    def on_Validate_Date(self, entry_name, new_value):
        """
        Cette fonction vérifie que l'heure entrée par l'utilisateur est bien formatée.
        Cette date doit être de la forme HHMMSS
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        print('OnValidateDate')
        print(entry_name)
        entry = self.nametowidget(entry_name)
        # Check the hours between 0 an 24, check the minutes between 0 and 59, check the seconds between 0 and 59 and chek the date lenght that should be 6 digits
        x = re.search("(?=^(2[0-3]|1[0-9]|0[0-9]))(?=^..[0-59])(?=^....[0-59])(?=[0-9]{6}$)", new_value)

        if x:
            print("Yes, there is at least one match!")
            entry.configure(background = '#98FB98')
        else:
            print("No match")
            entry.configure(background='#FFBCC1')
            return True

        return True

    def on_Validate_Est_Magn(self, entry_name, new_value):
        """
        Cette fonction vérifie que la valeur de l'Est magnétique entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre 0 et 400 (400 non inclus)
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        entry = self.nametowidget(entry_name)

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Angle(new_value))

            if (0 <= new_value and new_value < 400):
                print('New value' + str(new_value))
                entry.configure(background="#98FB98")
            else:
                entry.configure(background="#FFBCC1")

        except ValueError:
            entry.configure(background="#FFBCC1")
            return True

        return True

    def on_Validate_Angle(self, entry_name, new_value):
        """
        Cette fonction vérifie que la valeur de l'angle entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre 0 et 400 (400 non inclus)
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        Si l'entrée est correcte, cette fonction calcule automatiquement les valeurs des angles suivant et remplis les champs.
        """
        entry = self.nametowidget(entry_name)

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Angle(new_value))

            if (0 <= new_value and new_value < 400):
                print('New value' + str(new_value))
                entry.configure(background="#98FB98")

            else:
                entry.configure(background='#FFBCC1')

        except ValueError:
            entry.configure(background="#FFBCC1")
            return True

        if(new_value):
            print(self.probe_Up)
            if self.probe_Up is True:
                self.text_angle_2.config(text = self.format_Angle(float(new_value) - 1.5))
                self.text_angle_3.config(text = self.format_Angle(float(new_value) + 1.5))
            else:
                self.text_angle_2.config(text = self.format_Angle(float(new_value) + 1.5))
                self.text_angle_3.config(text = self.format_Angle(float(new_value) - 1.5))
            self.text_angle_4.config(text = self.format_Angle(new_value))

        return True

    def on_Validate_Magn_Value(self, entry_name, new_value):
        """
        Cette fonction vérifie que la valeur du magnétisme entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre -9999.9 et +9999.9
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        print('on_Validate_Magn_Value')
        entry = self.nametowidget(entry_name)
        entry.configure(background = "#98FB98")

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Magn_Value(new_value))

            if (-9999.9 <= new_value and new_value <= 9999.9):
                entry.configure(background="#98FB98")
            else:
                entry.configure(background="#FFBCC1")

        except ValueError:
            entry.configure(background = '#FFBCC1')
            return True

        return True     

    def get_Data(self):
        """
        Cette fonction retoune un dicionnaire contenant toutes les données du tableau saisi par l'utilisteur.
        """
        self.dictionnary_Data_Values = {
            'time_1' : self.time_1_Entry.get(),
            'time_2' : self.time_2_Entry.get(),
            'time_3' : self.time_3_Entry.get(),
            'time_4' : self.time_4_Entry.get(),
            'angle_1' : self.angle_1_Entry.get(),
            'angle_2' : self.text_angle_2.cget('text'),
            'angle_3' : self.text_angle_3.cget('text'),
            'angle_4' : self.text_angle_4.cget('text'),
            'magn_Value_1' : self.magn_Value_1_Entry.get(),
            'magn_Value_2' : self.magn_Value_2_Entry.get(),
            'magn_Value_3' : self.magn_Value_3_Entry.get(),
            'magn_Value_4' : self.magn_Value_4_Entry.get(),
            'est_Magn' : self.est_Magn_Entry.get()
        }
        return(self.dictionnary_Data_Values)

    def update_Data(self, dictionnary_Data):
        """
        Cette fonction remplis automatiquement les champs d'entrées du firmulaire avec les données passées en paramètre.
        """
        self.time_1_Var.set(dictionnary_Data['time_1']),
        self.time_2_Var.set(dictionnary_Data['time_2']),
        self.time_3_Var.set(dictionnary_Data['time_3']),
        self.time_4_Var.set(dictionnary_Data['time_4']),
        self.angle_1_Var.set(dictionnary_Data['angle_1']),
        self.text_angle_2.config(text = dictionnary_Data['angle_2']),
        self.text_angle_3.config(text = dictionnary_Data['angle_3']),
        self.text_angle_4.config(text = dictionnary_Data['angle_4']),
        self.magn_Value_1_Var.set(dictionnary_Data['magn_Value_1']),
        self.magn_Value_2_Var.set(dictionnary_Data['magn_Value_2']),
        self.magn_Value_3_Var.set(dictionnary_Data['magn_Value_3']),
        self.magn_Value_4_Var.set(dictionnary_Data['magn_Value_4']),
        self.est_Magn_Var.set(dictionnary_Data['est_Magn'])

    def format_Angle(self, value):
        """
        This function get a float and return a string with 4 digits after the comma, including the 0
        :return:
        """
        return(str(format(value, '.4f')))
    
    def format_Magn_Value(self, value):
        """
        This function get a float and return a string with 1 digits after the comma, including the 0
        :return:
        """
        return(str(format(value, '.1f')))

##
# class Entry_Angles_From_Target
#
# Cette classe décrit les champs d'entrée pour saisir les angles lors des visées de la cible.
# Cette classe est instanciée une seule fois.
##
class Entry_Angles_From_Target(tk.Frame):
    def __init__(self):
        super(Entry_Angles_From_Target, self).__init__()
        self.configure(bg = 'Light Grey')

        self.bearing_Azimuth = None

        self.table_Opening_X = None
        self.table_Opening_Y = None
        self.table_Closing_X = None
        self.table_Closing_Y = None

        self.average_Angle_V1 = 0
        self.average_Angle_V2 = 0

        self.validate_Command_V1 = self.register(self.on_Validate_V1)
        self.validate_Command_V2 = self.register(self.on_Validate_V2)

        # Angles from the target
        ttk.Label(self, width = 10, background = 'Light Grey').grid(row = 1, column = 3)
        ttk.Label(self, width = 10, background = 'Light Grey').grid(row = 2, column = 3)
        ttk.Label(self, text='V1 sonde en haut', background = 'Light Grey').grid(row= 1 , column = 1, sticky = tk.E)
        ttk.Label(self, text='V1 sonde en bas', background = 'Light Grey').grid(row = 2, column = 1, sticky = tk.E)
        ttk.Label(self, text='V2 sonde en haut', background = 'Light Grey').grid(row = 1, column = 4, sticky = tk.E)
        ttk.Label(self, text='V2 sonde en bas', background = 'Light Grey').grid(row = 2, column = 4, sticky = tk.E)
        self.V1_Probe_Up_Var = tk.StringVar()
        self.V1_Probe_Down_Var = tk.StringVar()
        self.V2_Probe_Up_Var = tk.StringVar()
        self.V2_Probe_Down_Var = tk.StringVar()
        self.V1_Probe_Up_Entry = tk.Entry(self, validate = "focusout", textvariable = self.V1_Probe_Up_Var, bg = 'white', fg = 'black')
        self.V1_Probe_Down_Entry = tk.Entry(self, validate = "focusout", textvariable = self.V1_Probe_Down_Var, bg = 'white', fg = 'black')
        self.V2_Probe_Up_Entry = tk.Entry(self, validate = "focusout", textvariable = self.V2_Probe_Up_Var, bg = 'white', fg = 'black')
        self.V2_Probe_Down_Entry = tk.Entry(self, validate = "focusout", textvariable = self.V2_Probe_Down_Var, bg = 'white', fg = 'black')
        self.V1_Probe_Up_Entry.grid(row = 1, column = 2)
        self.V1_Probe_Down_Entry.grid(row = 2, column = 2)
        self.V2_Probe_Up_Entry.grid(row = 1, column = 5)
        self.V2_Probe_Down_Entry.grid(row = 2, column = 5)
        self.V1_Probe_Up_Entry.configure(validatecommand = (self.validate_Command_V1, "%W", "%P"))
        self.V1_Probe_Down_Entry.configure(validatecommand = (self.validate_Command_V1, "%W", "%P"))
        self.V2_Probe_Up_Entry.configure(validatecommand = (self.validate_Command_V2, "%W", "%P"))
        self.V2_Probe_Down_Entry.configure(validatecommand = (self.validate_Command_V2, "%W", "%P"))

    def set_Bearing_Azimuth(bearing_Azimuth):
        self.bearing_Azimuth = bearing_Azimuth

    def on_Validate_V1(self, entry_name, new_value):
        print('on_Validate')
        entry = self.nametowidget(entry_name)
        entry.configure(background='#98FB98')

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Angle(new_value))

            # Validate the entry by coloring the cell
            if(0 <= new_value and new_value < 400):
                pass
            
            else:
                entry.configure(background='#FFBCC1')
                return True

        except ValueError:
            entry.configure(background='#FFBCC1')
            return True

        # Compute values automatically
        try:
            if self.V1_Probe_Up_Entry.get() and self.V1_Probe_Down_Entry.get():
                angle_Average = round((((float(self.V1_Probe_Up_Entry.get()) + float(self.V1_Probe_Down_Entry.get())) / 2) + 100) - float(self.bearing_Azimuth), 5)
                # round up angle_average :
                angle_Average = (math.ceil(angle_Average * 10000)) / 10000

                self.average_Angle_V1 = angle_Average

                self.table_Opening_X.text_angle_1.config(text = self.format_Angle(angle_Average))
                self.table_Opening_X.text_angle_2.config(text = self.format_Angle(angle_Average))
                self.table_Opening_X.text_angle_3.config(text = self.format_Angle((angle_Average - 200) % 400))
                self.table_Opening_X.text_angle_4.config(text = self.format_Angle((angle_Average - 200) % 400))

                self.table_Opening_Y.text_angle_1.config(text = self.format_Angle((angle_Average - 300) % 400))
                self.table_Opening_Y.text_angle_2.config(text = self.format_Angle((angle_Average - 300) % 400))
                self.table_Opening_Y.text_angle_3.config(text = self.format_Angle((angle_Average - 100) % 400))
                self.table_Opening_Y.text_angle_4.config(text = self.format_Angle((angle_Average - 100) % 400))

        except ValueError:
            pass        

        return True

    def on_Validate_V2(self, entry_name, new_value):
        print('on_Validate')
        entry = self.nametowidget(entry_name)
        entry.configure(background='#98FB98')

        try:
            new_value = float(new_value)
            entry.delete(0, 'end')
            entry.insert(0, self.format_Angle(new_value))

            # Validate the entry by coloring the cell
            if(0 <= new_value and new_value < 400):
                pass

            else:
                entry.configure(background='#FFBCC1')
                return True

        except ValueError:
            entry.configure(background='#FFBCC1')
            return True

        # Compute values automatically
        try:
            if self.V2_Probe_Up_Entry.get() and self.V2_Probe_Down_Entry.get():
                angle_Average = round((((float(self.V2_Probe_Up_Entry.get()) + float(self.V2_Probe_Down_Entry.get())) / 2) + 100) - float(self.bearing_Azimuth), 5)
                # round up angle_average :
                angle_Average = (math.ceil(angle_Average * 10000)) / 10000

                self.average_Angle_V2 = ((float(self.V2_Probe_Up_Entry.get()) + float(self.V2_Probe_Down_Entry.get())) / 2) + 100

                self.table_Closing_X.text_angle_1.config(text = self.format_Angle(angle_Average))
                self.table_Closing_X.text_angle_2.config(text = self.format_Angle(angle_Average))
                self.table_Closing_X.text_angle_3.config(text = self.format_Angle((angle_Average - 200) % 400))
                self.table_Closing_X.text_angle_4.config(text = self.format_Angle((angle_Average - 200) % 400))

                self.table_Closing_Y.text_angle_1.config(text = self.format_Angle((angle_Average - 300) % 400))
                self.table_Closing_Y.text_angle_2.config(text = self.format_Angle((angle_Average - 300) % 400))
                self.table_Closing_Y.text_angle_3.config(text = self.format_Angle((angle_Average - 100) % 400))
                self.table_Closing_Y.text_angle_4.config(text = self.format_Angle((angle_Average - 100) % 400))

        except ValueError:
            pass

        return True

    def get_Data(self):
        self.dictionnary_Data_Values = {
            'V1_Probe_Up' : self.V1_Probe_Up_Var.get(),
            'V1_Probe_Down' : self.V1_Probe_Down_Var.get(),
            'V2_Probe_Up' : self.V2_Probe_Up_Var.get(),
            'V2_Probe_Down' : self.V2_Probe_Down_Var.get(),
            'angle_From_Target_V1' : self.average_Angle_V1,
            'angle_From_Target_V2' : self.average_Angle_V2
        }   
        return(self.dictionnary_Data_Values)

    def update_Data(self, dictionnary_Data):
        self.V1_Probe_Up_Var.set(dictionnary_Data['V1_Probe_Up']),
        self.V1_Probe_Down_Var.set(dictionnary_Data['V1_Probe_Down']),
        self.V2_Probe_Up_Var.set(dictionnary_Data['V2_Probe_Up']),
        self.V2_Probe_Down_Var.set(dictionnary_Data['V2_Probe_Down']),
        self.average_Angle_V1 = dictionnary_Data['angle_From_Target_V1'],
        self.average_Angle_V2 = dictionnary_Data['angle_From_Target_V2']

    def format_Angle(self, value):
        """
        This function get a float and return a string with 4 digits after the comma, including the 0
        :return:
        """
        return(str(format(value, '.4f')))

##
# class Entry_Header
#
# Cette classe décrit l'affichage des information de la station qui se trouvent dans l'entête de la fenêtre.
# Ces information sont issues du fichier de configuration de l'outil.
# De plus cette classe contient un champ d'entré pour la date, qui est éditable.
# Cette classe est instanciée une seule fois.
##
class Entry_Header(tk.Frame):
    def __init__(self):
        super(Entry_Header, self).__init__()
        self.configure(bg = 'Light Grey')

        self.validate_Command_Date = self.register(self.on_Validate_Date)
        self.today_Date = datetime.today().strftime('%d/%m/%y')

        ttk.Label(self, background = 'Light Grey', width = 10).grid(row = 1, column = 3)
        ttk.Label(self, background = 'Light Grey', text='Station').grid(row = 2, column = 1, sticky = tk.E)
        ttk.Label(self, background = 'Light Grey', text='Date (JJ/MM/AA)', width = 20, anchor = 'e').grid(row = 1, column = 1)
        ttk.Label(self, background = 'Light Grey', text='corr. mesures de F').grid(row = 3, column = 1, sticky = tk.E)
        ttk.Label(self, background = 'Light Grey', text='angle de rotation').grid(row = 3, column = 4, sticky = tk.E)
        ttk.Label(self, background = 'Light Grey', text='Azimut repère').grid(row = 2, column = 4, sticky = tk.E)

        self.station_var = tk.StringVar()
        self.date_var = tk.StringVar(value = self.today_Date)
        self.correction_F_Measurement_Var = tk.StringVar()
        self.rotation_Angle_Var = tk.StringVar()
        self.bearing_Azimuth_Var = tk.StringVar()

        self.text_station = ttk.Label(self, width = 20, text = self.station_var.get())
        self.text_Correction_F_Measurement = ttk.Label(self, width = 20, text = self.correction_F_Measurement_Var.get())
        self.text_Rotation_Angle = ttk.Label(self, width = 20, text = self.rotation_Angle_Var.get())
        self.text_Bearing_Azimuth = ttk.Label(self, width = 20, text = self.bearing_Azimuth_Var.get())

        self.text_station.grid(row = 2, column = 2)
        self.text_Correction_F_Measurement.grid(row = 3, column = 2)
        self.text_Rotation_Angle.grid(row = 3, column = 5)
        self.text_Bearing_Azimuth.grid(row = 2, column = 5)

        self.text_station.config(anchor = 'center')
        self.text_Correction_F_Measurement.config(anchor = 'center')
        self.text_Rotation_Angle.config(anchor = 'center')
        self.text_Bearing_Azimuth.config(anchor = 'center')

        
        self.text_station.configure(background = "white")
        self.text_Correction_F_Measurement.configure(background = "white")
        self.text_Rotation_Angle.configure(background = "white")
        self.text_Bearing_Azimuth.configure(background = "white")

        self.date_entry = tk.Entry(self, validate = "focusout", textvariable = self.date_var, bg = 'yellow', fg = 'black')
        self.date_entry.grid(row = 1, column = 2)
        self.date_entry.configure(validatecommand = (self.validate_Command_Date, "%W", "%P"))
    
    def get_Data(self):
        self.dictionnary_Data_Values = {
            'station' : self.text_station.cget('text'),
            'date' : self.date_var.get(),
            'correction_F_Measurement' : self.text_Correction_F_Measurement.cget('text'),
            'rotation_Angle' : self.text_Rotation_Angle.cget('text'),
            'bearing_Azimuth' : self.text_Bearing_Azimuth.cget('text')
        }

        return(self.dictionnary_Data_Values)
    
    def update_Data(self, dictionnary_Data):
        self.date_var.set(dictionnary_Data['date'])
        self.text_station.config(text= dictionnary_Data['station'])
        self.text_Correction_F_Measurement.config(text = dictionnary_Data['correction_F_Measurement'])
        self.text_Rotation_Angle.config(text = dictionnary_Data['rotation_Angle'])
        self.text_Bearing_Azimuth.config(text = dictionnary_Data['bearing_Azimuth'])

    def on_Validate_Date(self, entry_name, new_value):
        """
        Cette fonction vérifie que la date entrée par l'utilisateur est bien formatée.
        Cette date doit être de la forme JJ/MM/AA
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        entry = self.nametowidget(entry_name)
        x = re.search("(?=^(3[0-1]|2[0-9]|1[0-9]|0[0-9]))(?=^...1[0-2]|^...0[0-9])(?=^......[0-99])(?=[0-9'/']{8}$)", new_value)

        if x:
            print("Yes, there is at least one match!")
            entry.configure(background = '#98FB98')

        else:
            print("No match")
            entry.configure(background='#FFBCC1')
            return True

        return True


##
# class Text_Frame
#
# Cette classe génère une frame contenant un texte.
# Celà permet de générer des textes qui peuvent se placer où l'on veut dans la fenêtre de l'interface graphique.
# Elle est utilisée pour afficher les titres au-dessus des tableaux. Elle est instanciée quatre fois.
##
class Text_Frame(tk.Frame):
    def __init__(self, text):
        super(Text_Frame, self).__init__()
        ttk.Label(self, text = text, background = 'Light Grey').grid(row = 1, column = 1)


##
# class Buttons_Frame
#
# Cette classe contient les deux boutons "ENREGISTRER" et "charger une masabs", qui sont les deux fonctionnalités de l'interface graphique.
# Elle est instanciée une seule fois.
##
class Buttons_Frame(tk.Frame):
    def __init__(self, save_button_clicked, load_Button_Clicked):
        super(Buttons_Frame, self).__init__()
        self.configure(bg = 'Light Grey')
        self.space = tk.Label(self, background = 'Light Grey')
        self.space.grid(row = 2, column = 1)
        self.space.config(height = 1)
        self.save_button = ttk.Button(self, text='ENREGISTRER', command = save_button_clicked, width = 20)
        self.load_button = ttk.Button(self, text='charger une mesabs', command = load_Button_Clicked, width = 20)
        self.save_button.grid(row=1, column=1)
        self.load_button.grid(row=3, column=1)