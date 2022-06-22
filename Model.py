import configparser
import re
import os
from os.path import exists

##
# class Model
#
# Cette classe est la classe Model de l'architecture logicielle Modèle - Vue - controlleur.
# Elle contient deux fonction principaes :
# - fonction save_Data, qui enregistre la mesabs dans un fichier texte.
# - fonction read_Mesabs, qui ouvre une mesabs déjà enregistrée à partir d'un fochier texte pour pouvoir l'éditer.
##
class Model:
    def __init__(self):
        self.table_metadata = {}
        self.table_Angles_From_Target = {}
        self.data_Sequence_1_X = {}
        self.data_Sequence_1_Y = {}
        self.data_Sequence_2_X = {}
        self.data_Sequence_2_Y = {}
        self.data_Calibration_Opening_Probe_Up = {}
        self.data_Calibration_Opening_Probe_Down = {}
        self.data_Calibration_Closing_Probe_Up = {}
        self.data_Calibration_Closing_Probe_Down = {}

        self.site = ''
        self.correction_F = ''
        self.rotation_Angle = ''   
        self.bearing_Azimuth = ''

        self.opening_Calibration_X = None
        self.closing_Calibration_X = None

        # set the controller
        self.controller = None

        self.file_Name = ''
        self.loaded_File_Name = ''

    def load_config_file(self):
        """
        Cette fonction charge les information présentes dans le fichier de configuration.
        Si le fichier est inexistant ou contient des erreurs alors un message d'erreur appraît dans l'interface graphique.
        """
        if not exists('config.txt'):
            print('MODEL : ERROR, no config file')
            self.controller.show_Error_Message(text = 'Fichier de config inexistant\nVeuillez créer le fichier config.txt dans le même répertoire que les scripts Python.')
            return True

        self.config = configparser.ConfigParser()
        self.config.read('config.txt')

        if (self.config.has_option('Station_Configuration', 'Site') and
            self.config.has_option('Station_Configuration', 'Correction_F') and
            self.config.has_option('Station_Configuration', 'Rotation_Angle') and
            self.config.has_option('Station_Configuration', 'Bearing_Azimuth') and
            self.config.has_option('Software_Configuration', 'Saving_Directory_Path')):
            pass
            
        else:
            print('MODEL : ERROR, errors existing inside the config file.')
            self.controller.show_Error_Message(text = 'Erreur dans la fichier de configuration config.txt\n\nVeuillez l\'éditer.')
            return True

        self.station_Configuration = self.config['Station_Configuration']
        self.software_Configuration = self.config['Software_Configuration']

        self.site = self.station_Configuration['Site']
        self.correction_F = self.station_Configuration['Correction_F']
        self.rotation_Angle = self.station_Configuration['Rotation_Angle']     
        self.bearing_Azimuth = self.station_Configuration['Bearing_Azimuth']

        self.saving_Directory_Path = self.software_Configuration['Saving_Directory_Path']

    def set_Controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def save_Data(self):
        """
        Cette fonction récupère toutes le données de l'interface graphique puis les formatte avec la bonne syntaxe pour les inscrire dans un fichier texte.
        Après la suvegarde une fenêtre s'affiche dans l'interface graphique pour confirmer ou infirmer l'enregistrement
        """

        if not self.validate_Data():
            self.controller.show_Error_Message(text = 'Erreur, une ou plusieurs valeurs sont erronées.')
            return True

        try :
            # Si une mesabs a déjà été chargée, supprimer cette mesabs.
            if self.loaded_File_Name != '':
                os.remove(self.loaded_File_Name) 

            mesabs_Date = self.table_metadata['date']
            mesabs_Hour_First_Measurement = self.data_Calibration_Opening_Probe_Up['time_1'][0:2]

            # file name : path + 're' + month + day + hour + year
            self.file_Name = self.saving_Directory_Path + '/re' + mesabs_Date[3:5] + mesabs_Date[0:2] + mesabs_Hour_First_Measurement + mesabs_Date[6:8] + '.' + self.site
            
            with open(self.file_Name , 'w') as file:
                file.write(' ' + self.table_metadata['station'] + ' ' + self.format_Date(self.table_metadata['date']) + '\n\n')
                file.write('correction sonde\n')
                file.write(self.format_F_Correction(self.table_metadata['correction_F_Measurement']) + '\n\n')
                file.write('angle de rotation\n')
                file.write(self.format_Rotation_Angle(self.table_metadata['rotation_Angle']) + '\n\n')
                file.write('visees balise\n')
                file.write(self.format_Target_Angle(self.table_metadata['bearing_Azimuth']) + '\n')
                file.write(self.format_Angle(self.table_Angles_From_Target['V1_Probe_Up']) + ' ' + self.format_Angle(self.table_Angles_From_Target['V1_Probe_Down']) + '\n')
                file.write(self.format_Angle(self.table_Angles_From_Target['V2_Probe_Up']) + ' ' + self.format_Angle(self.table_Angles_From_Target['V2_Probe_Down']) + '\n\n')

                file.write('Est magnetique ouverture\n')
                file.write(self.format_Angle(self.data_Calibration_Opening_Probe_Up['est_Magn']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Down['est_Magn']) + '\n\n')

                file.write('etalonnage ouverture\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Up['time_1']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Up['angle_1']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Up['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Up['time_2']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Up['angle_2']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Up['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Up['time_3']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Up['angle_3']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Up['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Up['time_4']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Up['angle_4']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Up['magn_Value_4']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Down['time_1']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Down['angle_1']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Down['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Down['time_2']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Down['angle_2']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Down['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Down['time_3']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Down['angle_3']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Down['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Opening_Probe_Down['time_4']) + ' ' + self.format_Angle(self.data_Calibration_Opening_Probe_Down['angle_4']) + (' ') + self.format_Magn_Value(self.data_Calibration_Opening_Probe_Down['magn_Value_4']) + '\n\n')                
                                
                file.write('Est magnetique fermeture\n')
                file.write(self.format_Angle(self.data_Calibration_Closing_Probe_Up['est_Magn']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Down['est_Magn']) + '\n\n')

                file.write('etalonnage fermeture\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Up['time_1']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Up['angle_1']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Up['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Up['time_2']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Up['angle_2']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Up['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Up['time_3']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Up['angle_3']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Up['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Up['time_4']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Up['angle_4']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Up['magn_Value_4']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Down['time_1']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Down['angle_1']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Down['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Down['time_2']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Down['angle_2']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Down['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Down['time_3']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Down['angle_3']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Down['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Calibration_Closing_Probe_Down['time_4']) + ' ' + self.format_Angle(self.data_Calibration_Closing_Probe_Down['angle_4']) + (' ') + self.format_Magn_Value(self.data_Calibration_Closing_Probe_Down['magn_Value_4']) + '\n')

                file.write('\nX serie 1\n')
                file.write(self.format_Time(self.data_Sequence_1_X['time_1']) + ' ' + self.format_Angle(self.data_Sequence_1_X['angle_1']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_X['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_X['time_2']) + ' ' + self.format_Angle(self.data_Sequence_1_X['angle_2']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_X['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_X['time_3']) + ' ' + self.format_Angle(self.data_Sequence_1_X['angle_3']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_X['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_X['time_4']) + ' ' + self.format_Angle(self.data_Sequence_1_X['angle_4']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_X['magn_Value_4']) + '\n')

                file.write('\nY serie 1\n')
                file.write(self.format_Time(self.data_Sequence_1_Y['time_1']) + ' ' + self.format_Angle(self.data_Sequence_1_Y['angle_1']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_Y['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_Y['time_2']) + ' ' + self.format_Angle(self.data_Sequence_1_Y['angle_2']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_Y['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_Y['time_3']) + ' ' + self.format_Angle(self.data_Sequence_1_Y['angle_3']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_Y['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Sequence_1_Y['time_4']) + ' ' + self.format_Angle(self.data_Sequence_1_Y['angle_4']) + (' ') + self.format_Magn_Value(self.data_Sequence_1_Y['magn_Value_4']) + '\n')

                file.write('\nX serie 2\n')
                file.write(self.format_Time(self.data_Sequence_2_X['time_1']) + ' ' + self.format_Angle(self.data_Sequence_2_X['angle_1']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_X['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_X['time_2']) + ' ' + self.format_Angle(self.data_Sequence_2_X['angle_2']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_X['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_X['time_3']) + ' ' + self.format_Angle(self.data_Sequence_2_X['angle_3']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_X['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_X['time_4']) + ' ' + self.format_Angle(self.data_Sequence_2_X['angle_4']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_X['magn_Value_4']) + '\n')

                file.write('\nY serie 2\n')
                file.write(self.format_Time(self.data_Sequence_2_Y['time_1']) + ' ' + self.format_Angle(self.data_Sequence_2_Y['angle_1']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_Y['magn_Value_1']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_Y['time_2']) + ' ' + self.format_Angle(self.data_Sequence_2_Y['angle_2']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_Y['magn_Value_2']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_Y['time_3']) + ' ' + self.format_Angle(self.data_Sequence_2_Y['angle_3']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_Y['magn_Value_3']) + '\n')
                file.write(self.format_Time(self.data_Sequence_2_Y['time_4']) + ' ' + self.format_Angle(self.data_Sequence_2_Y['angle_4']) + (' ') + self.format_Magn_Value(self.data_Sequence_2_Y['magn_Value_4']) + '\n')
            
            print("mesabs saved to " + self.file_Name)
            
            self.controller.show_Validation_Message('Mesabs enregistrée sous\n' + self.file_Name)

        except ValueError:
            self.controller.show_Error_Message(text = 'Erreur, enregistrement dans un fichier impossible')
            return False

    def read_Mesabs_From_file(self, filename):

        self.loaded_File_Name = filename
        
        with open(filename, 'r') as file:

            lines = file.readlines()

            self.table_metadata = {
                'station' : lines[0][1:4],
                'date' : lines[0][5:7] + '/' + lines[0][8:10] + '/' + lines[0][11:13],
                'correction_F_Measurement' : lines[3][0:6],
                'rotation_Angle' : lines[6][1:4],
                'bearing_Azimuth' : lines[9][1:8],
            }
            self.table_Angles_From_Target = {
                'V1_Probe_Up' : lines[10][0:8],
                'V1_Probe_Down' : lines[10][9:17],
                'V2_Probe_Up' : lines[11][0:8],
                'V2_Probe_Down' : lines[11][9:17],
                'angle_From_Target_V1' : '00.0000',
                'angle_From_Target_V2' : '00.0000'
            }
            self.data_Sequence_1_X = {
                'time_1' : lines[40][0:2] + lines[40][3:5] + lines[40][6:8],
                'time_2' : lines[41][0:2] + lines[41][3:5] + lines[41][6:8],
                'time_3' : lines[42][0:2] + lines[42][3:5] + lines[42][6:8],
                'time_4' : lines[43][0:2] + lines[43][3:5] + lines[43][6:8],
                'angle_1' : lines[40][9:16],
                'angle_2' : lines[41][9:16],
                'angle_3' : lines[42][9:16],
                'angle_4' : lines[43][9:16],
                'magn_Value_1' : lines[40][19:25],
                'magn_Value_2' : lines[41][19:25],
                'magn_Value_3' : lines[42][19:25],
                'magn_Value_4' : lines[43][19:25]
            }
            self.data_Sequence_1_Y = {
                'time_1' : lines[46][0:2] + lines[46][3:5] + lines[46][6:8],
                'time_2' : lines[47][0:2] + lines[47][3:5] + lines[47][6:8],
                'time_3' : lines[48][0:2] + lines[48][3:5] + lines[48][6:8],
                'time_4' : lines[49][0:2] + lines[49][3:5] + lines[49][6:8],
                'angle_1' : lines[46][9:16],
                'angle_2' : lines[47][9:16],
                'angle_3' : lines[48][9:16],
                'angle_4' : lines[49][9:16],
                'magn_Value_1' : lines[46][19:25],
                'magn_Value_2' : lines[47][19:25],
                'magn_Value_3' : lines[48][19:25],
                'magn_Value_4' : lines[49][19:25]
            }
            self.data_Sequence_2_X = {
                'time_1' : lines[52][0:2] + lines[52][3:5] + lines[52][6:8],
                'time_2' : lines[53][0:2] + lines[53][3:5] + lines[53][6:8],
                'time_3' : lines[54][0:2] + lines[54][3:5] + lines[54][6:8],
                'time_4' : lines[55][0:2] + lines[55][3:5] + lines[55][6:8],
                'angle_1' : lines[52][9:16],
                'angle_2' : lines[53][9:16],
                'angle_3' : lines[54][9:16],
                'angle_4' : lines[55][9:16],
                'magn_Value_1' : lines[52][19:25],
                'magn_Value_2' : lines[53][19:25],
                'magn_Value_3' : lines[54][19:25],
                'magn_Value_4' : lines[55][19:25]
            }
            self.data_Sequence_2_Y = {
                'time_1' : lines[58][0:2] + lines[58][3:5] + lines[58][6:8],
                'time_2' : lines[59][0:2] + lines[59][3:5] + lines[59][6:8],
                'time_3' : lines[60][0:2] + lines[60][3:5] + lines[60][6:8],
                'time_4' : lines[61][0:2] + lines[61][3:5] + lines[61][6:8],
                'angle_1' : lines[58][9:16],
                'angle_2' : lines[59][9:16],
                'angle_3' : lines[60][9:16],
                'angle_4' : lines[61][9:16],
                'magn_Value_1' : lines[58][19:25],
                'magn_Value_2' : lines[59][19:25],
                'magn_Value_3' : lines[60][19:25],
                'magn_Value_4' : lines[61][19:25]
            }
            self.data_Calibration_Opening_Probe_Up = {
                'time_1' : lines[17][0:2] + lines[17][3:5] + lines[17][6:8],
                'time_2' : lines[18][0:2] + lines[18][3:5] + lines[18][6:8],
                'time_3' : lines[19][0:2] + lines[19][3:5] + lines[19][6:8],
                'time_4' : lines[20][0:2] + lines[20][3:5] + lines[20][6:8],
                'angle_1' : lines[17][9:16],
                'angle_2' : lines[18][9:16],
                'angle_3' : lines[19][9:16],
                'angle_4' : lines[20][9:16],
                'magn_Value_1' : lines[17][19:25],
                'magn_Value_2' : lines[18][19:25],
                'magn_Value_3' : lines[19][19:25],
                'magn_Value_4' : lines[20][19:25],
                'est_Magn' : lines[14][0:8]
            }
            self.data_Calibration_Opening_Probe_Down = {
                'time_1' : lines[21][0:2] + lines[21][3:5] + lines[21][6:8],
                'time_2' : lines[22][0:2] + lines[22][3:5] + lines[22][6:8],
                'time_3' : lines[23][0:2] + lines[23][3:5] + lines[23][6:8],
                'time_4' : lines[24][0:2] + lines[24][3:5] + lines[24][6:8],
                'angle_1' : lines[21][9:16],
                'angle_2' : lines[22][9:16],
                'angle_3' : lines[23][9:16],
                'angle_4' : lines[24][9:16],
                'magn_Value_1' : lines[21][19:25],
                'magn_Value_2' : lines[22][19:25],
                'magn_Value_3' : lines[23][19:25],
                'magn_Value_4' : lines[24][19:25],
                'est_Magn' : lines[14][8:17]
            }
            self.data_Calibration_Closing_Probe_Up = {
                'time_1' : lines[30][0:2] + lines[30][3:5] + lines[30][6:8],
                'time_2' : lines[31][0:2] + lines[31][3:5] + lines[31][6:8],
                'time_3' : lines[32][0:2] + lines[32][3:5] + lines[32][6:8],
                'time_4' : lines[33][0:2] + lines[33][3:5] + lines[33][6:8],
                'angle_1' : lines[30][9:16],
                'angle_2' : lines[31][9:16],
                'angle_3' : lines[32][9:16],
                'angle_4' : lines[33][9:16],
                'magn_Value_1' : lines[30][19:25],
                'magn_Value_2' : lines[31][19:25],
                'magn_Value_3' : lines[32][19:25],
                'magn_Value_4' : lines[33][19:25],
                'est_Magn' : lines[27][0:8]
            }
            self.data_Calibration_Closing_Probe_Down = {
                'time_1' : lines[34][0:2] + lines[34][3:5] + lines[34][6:8],
                'time_2' : lines[35][0:2] + lines[35][3:5] + lines[35][6:8],
                'time_3' : lines[36][0:2] + lines[36][3:5] + lines[36][6:8],
                'time_4' : lines[37][0:2] + lines[37][3:5] + lines[37][6:8],
                'angle_1' : lines[34][9:16],
                'angle_2' : lines[35][9:16],
                'angle_3' : lines[36][9:16],
                'angle_4' : lines[37][9:16],
                'magn_Value_1' : lines[34][19:25],
                'magn_Value_2' : lines[35][19:25],
                'magn_Value_3' : lines[36][19:25],
                'magn_Value_4' : lines[37][19:25],
                'est_Magn' : lines[27][8:17]
                }

            print("Mesabs " + filename + " loaded.")

    def validate_Data(self):
        """
        Cette fonction vérifie que toutes les données reçues de l'interface graphique sont valides.
        Elle est appelée avant l'enregistrement des données dans un fichier texte.
        Si au moins une des données est erronnée alors l'enregistrement n'a pas lieu et un massage d'erreur s'affiche dans l'interface graphique.
        """
        validation = False
        data_Tables = [
            self.data_Sequence_1_X,
            self.data_Sequence_1_Y,
            self.data_Sequence_2_X,
            self.data_Sequence_2_Y,
            self.data_Calibration_Opening_Probe_Up,
            self.data_Calibration_Opening_Probe_Down,
            self.data_Calibration_Closing_Probe_Up,
            self.data_Calibration_Closing_Probe_Down
        ]
        data_Tables_Calibrations = [
            self.data_Calibration_Opening_Probe_Up,
            self.data_Calibration_Opening_Probe_Down,
            self.data_Calibration_Closing_Probe_Up,
            self.data_Calibration_Closing_Probe_Down
        ]
        keys_Times = ['time_1', 'time_2', 'time_3', 'time_4']
        keys_Angles = ['angle_1', 'angle_2', 'angle_3', 'angle_4']
        keys_Magn_values = ['magn_Value_1' ,'magn_Value_2' ,'magn_Value_3' ,'magn_Value_4']
        keys_Angles_From_Target = ['V1_Probe_Up', 'V1_Probe_Down', 'V2_Probe_Up', 'V2_Probe_Down']

        # --- Check the tables data
        for data_Table in data_Tables:
            
            for key_time in keys_Times:
                validation = self.validate_Time(data_Table[key_time])

                if not validation :
                    print('MODEL : error in time')
                    return False

        for data_Table in data_Tables:
            
            for key_Angle in keys_Angles:
                validation = self.validate_Angle(data_Table[key_Angle])

                if not validation :
                    print('MODEL : error in angle')
                    return False

        for data_Table in data_Tables:
            
            for key_Magn_Value in keys_Magn_values:
                validation = self.validate_Magn_Value(data_Table[key_Magn_Value])

                if not validation :
                    print('MODEL : error in magnetic value')
                    return False
        
        # --- Check the Est magnetic measurements
        for data_Table_Calibration in data_Tables_Calibrations:
            validation = self.validate_Angle(data_Table_Calibration['est_Magn'])

            if not validation :
                print('MODEL : error in est magne')
                return False
        
        # --- Check the angles from the target
        for key in keys_Angles_From_Target:
            validation = self.validate_Angle(self.table_Angles_From_Target[key])

            if not validation :
                print('MODEL : error in angles from target')
                return False

        # --- Check the date
        validation = self.validate_Date(self.table_metadata['date'])

        if not validation:
                print('MODEL : error in date')
                return False

        return True
    
    def validate_Time(self, time):
        """
        Cette fonction vérifie que l'heure entrée par l'utilisateur est bien formatée.
        Cette date doit être de la forme HHMMSS
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        validation = re.search("(?=^(2[0-3]|1[0-9]|0[0-9]))(?=^..[0-59])(?=^....[0-59])(?=[0-9]{6}$)", time)
        return validation

    def validate_Date(self, date):
        """
        Cette fonction vérifie que la date entrée par l'utilisateur est bien formatée.
        Cette date doit être de la forme JJ/MM/AA
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        validation = re.search("(?=^(3[0-1]|2[0-9]|1[0-9]|0[0-9]))(?=^...1[0-2]|^...0[0-9])(?=^......[0-99])(?=[0-9'/']{8}$)", date)
        return validation
        
    def validate_Angle(self, angle):
        """
        Cette fonction vérifie que la valeur de l'angle entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre 0 et 400 (400 non inclus)
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        Si l'entrée est correcte, cette fonction calcule automatiquement les valeurs des angles suivant et remplis les champs.
        """
        try:
            angle = float(angle)
            
            if (0 <= angle and angle < 400):
                return True

            return False

        except ValueError:
            return False

    def validate_Magn_Value(self, magn_Value):
        """
        Cette fonction vérifie que la valuer du magnétisme entrée par l'utilisateur est bien formatée.
        Cette valeur doit être comprise entre -9999.9 et +9999.9
        Si c'est la cas, l'entrée se colore en vert. Sinon elle se colore en rouge.
        """
        try:
            magn_Value = float(magn_Value)

            if (-9999.9 <= magn_Value and magn_Value < 9999.9):
                return True

            return False

        except ValueError:
            return False

    def format_Angle(self, value):
        """
        This function get a float and return a string with 4 digits after the comma, including the 0
        :return:
        """
        return("{:8.4f}".format(float(value)))

    def format_Target_Angle(self, value):
        """
        This function get a float and return a string with 5 digits after the comma, including the 0
        :return:
        """
        return("{:9.5f}".format(float(value)))

    def format_Rotation_Angle(self, value):
        """
        This function get a float and return a string with 4 digits after the comma, including the 0
        :return:
        """
        return("{:7.4f}".format(float(value)))

    def format_Magn_Value(self, value):
        """
        This function get a float and return a string with 6 digits before comma and 1 digits after comma, including the 0
        :return:
        """
        return("{:8.1f}".format(float(value)))

    def format_F_Correction(self, value):
        """
        This function get a float and return a string with 4 digits after the comma, including the 0
        :return:
        """
        return("{:5.2f}".format(float(value)))

    def format_Date(self, value):
        """
        Cette fonction retourne la date de la forme JJ/MM/AA en rempalçant les / par des espaces, soit JJ MM AA
        """
        return(value[0:2] + ' ' + value[3:5] + ' ' + value[6:8])

    def format_Time(self, value):
        """
        Cette fonction retourne l'heure de la forme HH/MM/SS en rempalçant les / par des espaces, soit HH MM SS
        """
        return(value[0:2] + ' ' + value[2:4] + ' ' + value[4:6])
