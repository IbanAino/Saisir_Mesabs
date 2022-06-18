##
# class Controller
#
# Cette classe est la classe Controller de l'architecture logicielle Modèle - Vue - controlleur.
# Elle se charge de faire transiter les commandes et les données entre le Modèle et la Vue.
##
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save_Data(self):
        """
        Save the data into a file
        :param data:
        :return:
        """
        self.model.table_metadata = self.view.entry_Header.get_Data()
        self.model.table_Angles_From_Target = self.view.entry_Angles_From_Target.get_Data()
        self.model.data_Sequence_1_X = self.view.opening_Calibration_X.get_Data()
        self.model.data_Sequence_1_Y = self.view.opening_Calibration_Y.get_Data()
        self.model.data_Sequence_2_X = self.view.closing_Calibration_X.get_Data()
        self.model.data_Sequence_2_Y = self.view.closing_Calibration_Y.get_Data()
        self.model.data_Calibration_Opening_Probe_Up = self.view.calibration_Opening_Probe_Up.get_Data()
        self.model.data_Calibration_Opening_Probe_Down = self.view.calibration_Opening_Probe_Down.get_Data()
        self.model.data_Calibration_Closing_Probe_Up = self.view.calibration_Closing_Probe_Up.get_Data()
        self.model.data_Calibration_Closing_Probe_Down = self.view.calibration_Closing_Probe_Down.get_Data()

        self.model.save_Data()

    def load_Station_Config(self):
        """
        Cette fonction envoie à l'interface graphique les données lues dans le fichier config de l'application afin de les afficher.
        Cette fonction n'est appelée qu'après l'instanciation de toutes le classes, car le fichier de config n'est lu qu'une fois le programme lancé.
        """
        self.model.load_config_file()
        
        self.view.site = self.model.site,
        self.view.correction_F = self.model.correction_F,
        self.view.rotation_Angle = self.model.rotation_Angle,
        self.view.bearing_Azimuth = self.model.bearing_Azimuth
        self.view.saving_Directory_Path = self.model.saving_Directory_Path
        self.view.update_Station_Config()

    def get_file_to_load(self, filename):
        """
        Cette foncation envoie au Model le fichier à lire, précédemment sélectionné dans le View.
        Le Model extrait les données du fichier texte.
        Les données sont ensuite renvoyées au View pour remplir les champs du formulaire
        """
        self.model.read_Mesabs_From_file(filename)

        self.view.opening_Calibration_X.update_Data(self.model.data_Sequence_1_X)
        self.view.opening_Calibration_Y.update_Data(self.model.data_Sequence_1_Y)
        self.view.closing_Calibration_X.update_Data(self.model.data_Sequence_2_X)
        self.view.closing_Calibration_Y.update_Data(self.model.data_Sequence_2_Y)

        self.view.calibration_Opening_Probe_Up.update_Data(self.model.data_Calibration_Opening_Probe_Up)
        self.view.calibration_Opening_Probe_Down.update_Data(self.model.data_Calibration_Opening_Probe_Down)
        self.view.calibration_Closing_Probe_Up.update_Data(self.model.data_Calibration_Closing_Probe_Up)
        self.view.calibration_Closing_Probe_Down.update_Data(self.model.data_Calibration_Closing_Probe_Down)

        self.view.entry_Angles_From_Target.update_Data(self.model.table_Angles_From_Target)

        self.view.entry_Header.update_Data(self.model.table_metadata)

    def show_Error_Message(self, text):
        """
        Cette fonction affiche un message d'erreur dans l'interface graphique avec un texte personnalisé.
        """
        self.view.show_Error_Message(text)

    def show_Validation_Message(self, text):
        """
        Cette fonction affiche un message de succès dans l'interface graphique avec un texte personnalisé.
        """
        self.view.show_Validation_Message(text)
