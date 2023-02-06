from dns_checker import DnsChecker, DnsCheckerFunctions
import os
import json
import time

parameters_path = '/home/ec2-user/data/parameters.json'


#Si on a bien reçu le fichier de paramétrages on peut commencer et le lire
if os.path.exists(parameters_path):
    with open(parameters_path, 'r') as p:
        parameters = json.load(p)
    
    #Si on a bien reçu le fichier avec les données, on peut commencer le traitement
    if os.path.exists(f"/home/ec2-user/data/data_file{parameters.get('file_suffix')}"):
        
        #DnsChecker est la classe principale qui gère toutes les requêtes et leu traitement
        if parameters.get('file_suffix') == '.xlsx':
            analysis = DnsChecker(file_extension=parameters.get('file_suffix'), column_name=parameters.get('column'), url_type=parameters.get('url_type'), sheet_name=parameters.get('sheet_name'), column_filter=parameters.get('filter'))
        else:
            analysis = DnsChecker(file_extension=parameters.get('file_suffix'), column_name=parameters.get('column'), url_type=parameters.get('url_type'), column_filter=parameters.get('filter'))
        
        analysis.run()
        
        #A la fin on supprime les fichiers qu'on a reçu
        os.remove('/home/ec2-user/data/parameters.json')
        os.remove(f"/home/ec2-user/data/data_file{parameters.get('file_suffix')}")
       
        