import tkinter as tk
import pandas as pd
import numpy as np
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import os
import json
import hashlib
import paramiko
import time
from tkinter import Menu, ttk
from pathlib import Path
from tkinter.messagebox import showerror, showinfo, YES


class GUIElbaDnsChecker:

    def __init__(self) -> None:
        
        """Constructeur de la classe : met en place les variables de base et les widgets par défaut de la classe
        """

        self.file_path = ''
        self.file_suffix = None
        self.sheet_name_selected = None
        self.column_selected = None
        self.filter_selected = None
        self.url_type = None
        self.password = None
        self.save_file = None
        self.save_file_label = None
        self.sheet_name_combo = None


        self.server_config_file = str(Path(__file__).parent / 'server_config.json')
        self.parameters_file = str(Path(__file__).parent / 'parameters.json')

        
        ###Window setup

        self.window = tk.Tk()
        #nom de la fenêtre
        self.window.title('DNS checker')
        #logo
        self.window.iconbitmap( Path(__file__).parent / 'logo_elba.ico')
        self.window.config(background='#020f3b')
        
        self.screen_width, self.screen_height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window_width, self.window_height = 1080, 720

        x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        y_cordinate = int((self.screen_height/2) - (self.window_height/2))
        self.window.geometry(f'{self.window_width}x{self.window_height}+{x_cordinate}+{y_cordinate}')
        
        ###Menubar

        self.menu_bar = tk.Menu(self.window, bg="#020f3b", fg="white")
        self.window.config(menu=self.menu_bar)
        
        self.key_menu = tk.Menu(self.menu_bar)
        self.key_menu.add_command(label='Set up a server', command=self.setup_server)
        self.key_menu.add_command(label='Server info', command=self.server_info)
        self.key_menu.add_command(label='Load key', command=self.load_key)
        self.key_menu.add_command(label='Configure your password', command=self.password_hash)
        self.key_menu.add_command(label='Compare passwords', command=self.compare_passwords)
        self.menu_bar.add_cascade(label="Config app", menu=self.key_menu)

        ###Select parameters and file frame

        self.select_param_frame = tk.Frame(self.window, bg="#020f3b")
        self.sheet_name_label = tk.Label(self.select_param_frame, font=("Courrier", 15), bg="#020f3b", fg="white")
        self.columns_name_label = tk.Label(self.select_param_frame, font=("Courrier", 15), bg="#020f3b", fg="white")
        self.filter_label = tk.Label(self.select_param_frame, font=("Courrier", 15), bg="#020f3b", fg="white")
       
        #
        self.select_file_frame = tk.Frame(self.window, bg="#020f3b")
        
        self.file_path_label = tk.Label(self.select_file_frame, font=("Courrier", 10), bg="#020f3b", fg="white")
        self.select_file_button = tk.Button(self.select_file_frame, text="Ajouter un fichier à traiter", font=("Courrier", 20), bg="#020f3b", fg="white", command=self.select_file).pack()
        self.file_path_label.pack()
        
        self.select_file_frame.pack(expand=YES)
        #
        self.sheet_name_label.grid(row=0, column=0)
        self.columns_name_label.grid(row=2, column=0)
        self.filter_label.grid(row=4, column=0)
    
        self.select_param_frame.pack(expand=YES)

        ###URL type frame

        self.url_type_frame = tk.Frame(self.window, bg="#020f3b")
        self.url_type_value = tk.StringVar()
        self.url_type_possibilities = ['url', 'website', 'domain']
        
        for x in range(len(self.url_type_possibilities)):
            tk.Radiobutton(self.url_type_frame, text=self.url_type_possibilities[x], variable=self.url_type_value, value=self.url_type_possibilities[x], font=("Courrier", 20), bg="#020f3b", fg='red').grid(row=0, column=x)    
    
        self.url_type_frame.pack()
        

        ###Saving frame

        self.save_frame = tk.Frame(self.window, bg="#020f3b")
        self.save_file_label = tk.Label(self.save_frame, font=("Courrier", 10), bg="#020f3b", fg="white")
        self.saving_button = tk.Button(self.save_frame, text="Enregistrer sous...", font=("Courrier", 20), bg="#020f3b", fg="white", command=self.save_as).pack()
        self.save_file_label.pack()
        self.save_frame.pack(expand=YES)
        
        ### Password frame

        self.password_frame = tk.Frame(self.window, bg="#020f3b")
        self.password_value = tk.StringVar()

        self.password_label = tk.Label(self.password_frame, text="Mot de passe :", font=("Courrier", 20), bg="#020f3b", fg="white").pack()
        self.password_input = tk.Entry(self.password_frame, textvariable=self.password_value, show='*', font=("Courrier", 15), bg="#020f3b", fg="white").pack()

        self.password_frame.pack(expand=YES)

        ###Start analysis frame

        self.analysis_frame = tk.Frame(self.window, bg="#020f3b")
        self.analysis_button = tk.Button(self.analysis_frame, text="Lancer l'analyse", font=("Courrier", 20), bg="#020f3b", fg="white", command=self.start_analysis).pack()
        self.analysis_frame.pack(expand=YES)

        self.window.mainloop()

    
    def select_file(self):
        """Fonction activée quand on clique sur le bouton choisir un fichier
        """
        self.file_path = str(tkinter.filedialog.askopenfilename(filetypes=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"))))
        self.file_suffix =Path(self.file_path).suffix 

        #Indique le nom du fichier sélectionné
        self.file_path_label['text'] = self.file_path
        
    
        if self.file_suffix == '.xlsx':
            #Si le fichier est un xlsx il faut choisir la feuille sur laquelle on travaille
            self.sheet_name_label['text'] = 'Quelle feuille voulez vous traiter ?'

            self.sheets_name_list = list(pd.ExcelFile(self.file_path).sheet_names)

            self.sheet_name = tk.StringVar()
            self.sheet_name_combo = ttk.Combobox(self.select_param_frame, values=self.sheets_name_list, textvariable=self.sheet_name, font=("Courrier", 10))
            self.sheet_name_combo.current(0)
            self.sheet_name_combo.grid(row=1, column=0)
            self.sheet_name_combo.bind('<<ComboboxSelected>>', self.get_sheet_name)


        elif self.file_suffix == '.csv':
            #Si le fichier est un csv on ne choisit pas la feuille, on détruit les widgets précedents et on passe à la sélection des options
            self.sheet_name_label['text'] = ''
            
            if self.sheet_name_combo != None:
                self.sheet_name_combo.destroy()
            
            #Lit le fichier
            self.df = pd.read_csv(self.file_path)
            self.select_parameters()
    
    def get_sheet_name(self, event):
        """Renvoie le nom de la feuille sélectionnée

        Args:
            event (_type_): l'utilisateur a cliqué sur une des options
        """
        self.sheet_name_selected = self.sheet_name.get()
        self.download_xlsx_df()
    
    def download_xlsx_df(self):
        #Lit le fichier et passe à la sélection des options
        self.df = pd.read_excel(self.file_path, self.sheet_name_selected)
        self.select_parameters()
        
        
    def select_parameters(self):
        """Permet de choisir les options : Nom de la colonne et filtre
        """
        
        self.columns_list = list(self.df.columns)
        
        ###
        self.columns_name_label['text'] = 'Sélectionnez la colonne contenant les urls : '
        
        self.column_name = tk.StringVar()
        self.combo_columns_name = ttk.Combobox(self.select_param_frame, values=self.columns_list, textvariable=self.column_name, font=("Courrier", 10))
        self.combo_columns_name.current(0)
        self.combo_columns_name.grid(row=3, column=0)

        self.combo_columns_name.bind('<<ComboboxSelected>>', self.get_column_name)
        
        ###
        self.filter_label['text'] = 'Sélectionnez une colonne à filtrer :'

        self.filter = tk.StringVar()
        self.combo_filter = ttk.Combobox(self.select_param_frame, values=self.columns_list, textvariable=self.filter, font=("Courrier", 10))
        self.combo_filter.current()
        self.combo_filter.grid(row=5, column=0)

        self.combo_filter.bind('<<ComboboxSelected>>', self.get_filter)

    def get_column_name(self, event):
        """Récupère le nom de la colonne

        Args:
            event (_type_): Une colonne a été choisie
        """
        self.column_selected = self.column_name.get()
    
    def get_filter(self, event):

        """Récupère le nom du filtre
        """

        self.filter_selected = self.filter.get()

    def save_as(self):

        """Activée quand on clique sur Enregistrer sur... et récupère le nom du fichier sélctionnéz
        """
       
        if self.file_suffix == '.csv':
            self.save_file = str(tkinter.filedialog.asksaveasfilename(initialdir=str(Path.home), filetypes=(("CSV file", "*.csv"), ("Excel file", "*.xlsx")),defaultextension=f"*{self.file_suffix}"))
        
        else:
            self.save_file = str(tkinter.filedialog.asksaveasfilename(initialdir=str(Path.home), filetypes=(("Excel file", "*.xlsx"), ("CSV file", "*.csv")),defaultextension=f"*{self.file_suffix}"))
       
        self.save_file_label['text'] = self.save_file    
           

    def start_analysis(self):

        """Activée quand on clique sur Lancer l'analyse
        """

        #Récupère la config du serveur
        
        if os.path.exists(self.server_config_file):
            with open(self.server_config_file, 'r') as f:
                self.server_config = json.load(f)

        #Récupère les valeurs manquantes

        self.url_type = self.url_type_value.get()
        self.password = self.password_value.get()

        #On vérifie qu'on a toutes les infos qu'il faut
        
        if (self.server_config.get('username') != None) and (self.server_config.get('hostname') != None) and (self.server_config.get('key_path') != None) and (self.server_config.get('key_password_hash') != None):
            if self.file_path != None:
                if os.path.exists(self.file_path):
                    if (self.file_suffix == '.xlsx')  or (self.file_suffix == '.csv'):
                        if ((self.file_suffix == '.xlsx') and (self.sheet_name_selected != None)) or ((self.file_suffix == '.csv') and (self.sheet_name_selected == None)):
                            if self.column_selected != None:
                                if (self.url_type != None) and (self.url_type != ''):
                                    if self.save_file != None:
                                        if self.server_config.get('key_password_hash') != None:
                                            if hashlib.md5(self.password.encode()).hexdigest() == self.server_config.get('key_password_hash'):
                                                
                                                #Si tout est bon on envoie la requête au serveur
                                                self.send_request()
                                            
                                            else:
                                                showerror(title='Erreur', message='Mot de passe incorrect')
                                        else:
                                            showerror(title='Erreur', message='Vous devez paramétrer le mot de passe de la clé dans Config')
                                    else:
                                        showerror(title='Erreur', message='Vous devez indiquer un fichier pour enregistrer les résultats')
                                else:
                                    showerror(title='Erreur', message="Vous devez sélectionner un type d'url")
                            else:
                                showerror(title='Erreur', message='Vous devez sélectionner une colonne')
                        else:
                            showerror(title='Erreur', message='Vous devez sélectionner une feuille')
                    else:
                        showerror(title='Erreur', message="Seuls les fichiers '.csv' ou '.xlsx' sont supportés")  
                else:
                    showerror(title='Erreur', message='Fichier introuvable')
            else:
                showerror(title='Erreur', message='Veuillez spécifier un fichier')
        else:
            showerror(title='Erreur', message='Veuillez configurer un serveur')

    def send_request(self):
        """Envoie la requête au serveur avec toutes les infos nécessaires et récupère la réponse
        """
        #Info à envoyer au serveur
        request_dict = {
            'file_suffix' : self.file_suffix,
            'column' : self.column_selected,
            'url_type' : self.url_type,
            'sheet_name' : self.sheet_name_selected,
            'filter' : self.filter_selected
        }

        #Ecriture du fichier de paramétrages
        with open(self.parameters_file, 'w') as f:
            json.dump(request_dict, f)
        
        showinfo(title='Analyse', message=f"Confirmez le démarrage de l'analyse :")
        #Début du chrono
        start_time = time.time()

        #Connexion en SSH au server
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.server_config.get('hostname'), username=self.server_config.get('username'), key_filename=self.server_config.get('key_path'), password=self.password)
        
        #Transfert des fichiers au serveur avec le protocole SFTP
        ftp_client=ssh_client.open_sftp()
        ftp_client.put(self.parameters_file,'/home/ec2-user/data/parameters.json')
        ftp_client.put(self.file_path,f'/home/ec2-user/data/data_file{self.file_suffix}')
        ftp_client.close()

        #Supprime le fichier de paramétrages une fois qu'il est envoyé
        if os.path.exists(self.parameters_file):
            os.remove(self.parameters_file)

        time.sleep(1)

        #Execute le script sur le serveur pour lancer l'analyse à partir des fichiers transférés
        stdin,stdout,stderr = ssh_client.exec_command('python3 dns_checker_server.py')
        
        #Afficher les erreurs dans le terminal si on le souhaite
        #print(f' exec script stdout : {stdout.read()}, \nstderr : {stderr.read()}')
        
        #On vérifie que le fichier existe avant de le récupérer
        files_list = ''

        while files_list.find(f'dns_checking{self.file_suffix}') == -1:
            
            stdin,stdout,stderr = ssh_client.exec_command('ls /home/ec2-user/data/')
            files_list = ((stdout.read()).decode())
            
            #On attend un peu avant de récupérer les résultats pour être sûr qu'ils soient bien enregistrés
            time.sleep(1)
            
        
        #On récupère le fichier résultat en SFTP, on le supprime du serveur et on se déconnecte
        ftp_client=ssh_client.open_sftp()
        ftp_client.get(f'/home/ec2-user/data/dns_checking{self.file_suffix}', self.save_file)
        
        
        time.sleep((time.time()-start_time)/10)

        ftp_client.remove(f'/home/ec2-user/data/dns_checking{self.file_suffix}')
        ftp_client.close()
        ssh_client.close()

        #Message de fin d'éxecution et fermeture de la fenêtre
        exec_time = (time.time() - start_time)

        stderr = stderr.read().decode()

        if stderr == '':
            stderr = 'None'

        if exec_time > 60:    
            showinfo("Analyse terminée", message=f"L'analyse est terminée\nLes résultats sont dans : {self.save_file} \nTemps d'éxecution : {np.round((exec_time/60),2)} minutes \nErreurs : {stderr}")
        else:
            showinfo("Analyse terminée", message=f"L'analyse est terminée\nLes résultats sont dans : {self.save_file} \nTemps d'éxecution : {np.round((exec_time),2)} secondes \nErreurs : {stderr}")
        
        self.window.destroy()


    def load_key(self):
        """Permet de changer de clé
        """
        self.server_key_path = tkinter.filedialog.askopenfilename()

        if os.path.exists(self.server_config_file):
            
            with open(self.server_config_file, 'r') as f:
                server_config_dict = json.load(f)

            if self.server_key_path !=  None:
                server_config_dict['key_path'] = self.server_key_path

            with open(self.server_config_file, 'w') as f:
                json.dump(server_config_dict, f)
    
    def password_hash(self):
        """Permet d'enregistrer un mdp pour permettre la connexion
        """
        
        if os.path.exists(self.server_config_file):
            
            with open(self.server_config_file, 'r') as f:
                server_config_dict = json.load(f)

            password_entry = tkinter.simpledialog.askstring(title='Password', prompt='Enter your password', show='*')
            
            if password_entry != None:
                hashed_password = hashlib.md5(password_entry.encode()).hexdigest()
                server_config_dict['key_password_hash'] = hashed_password

            with open(self.server_config_file, 'w') as f:
                json.dump(server_config_dict, f)

    def setup_server(self):
        
        """COnfiguration d'un nouveau serveur : Nouveaux hostname, username et clées, mot de passe réinitialisé
        """

        if os.path.exists(self.server_config_file):
            
            with open(self.server_config_file, 'r') as f:
                server_config_dict = json.load(f)

            server_config_dict['username'] = tkinter.simpledialog.askstring(title='Username', prompt='Enter new username')
            server_config_dict['hostname'] = tkinter.simpledialog.askstring(title='Hostname', prompt='Enter new hostname')
            
            showinfo(title='Key', message='Select your key')
            server_config_dict['key_path'] = tkinter.filedialog.askopenfilename()
            
            server_config_dict['key_password_hash'] = None
            
            showinfo(title='Reset', message='Your password has been reseted, you must configure it in order to use the app \nCheck server info to see if your informations are correct')
            

            with open(self.server_config_file, 'w') as f:
                json.dump(server_config_dict, f)

    def server_info(self):
        """Affiche les infos du serveur auquel on est connecté"""
        
        if os.path.exists(self.server_config_file):
            
            with open(self.server_config_file, 'r') as f:
                server_config_dict = json.load(f)

            showinfo(title='Server info', message=f'Username : {server_config_dict.get("username")} \nHostname : {server_config_dict.get("hostname")} \nPath towards key : {server_config_dict.get("key_path")} \nHashed password : {server_config_dict.get("key_password_hash")}')

    def compare_passwords(self):

        """Permet de vérifier le mot de passe enregistré
        """

        if os.path.exists(self.server_config_file):
            
            with open(self.server_config_file, 'r') as f:
                server_config_dict = json.load(f)

            password_to_compare = tkinter.simpledialog.askstring(title='Compare passwords', prompt='Enter the password you want to compare with the registered one', show='*')

            if password_to_compare != None:
                if hashlib.md5(password_to_compare.encode()).hexdigest() == server_config_dict.get('key_password_hash'):
                    showinfo(title='Compare passwords', message='Passwords are identical')
                else:
                    showinfo(title='Compare passwords', message='Passwords are different')

if __name__ == '__main__':
    app = GUIElbaDnsChecker()
