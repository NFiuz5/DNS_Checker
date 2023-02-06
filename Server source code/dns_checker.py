import pandas as pd
import json
import os
import dns
import dns.resolver
from pprint import pprint
from pathlib import Path

class DnsCheckerFunctions:

    def read_json_file(file):
        """Lit un fichier json

        Args:
            file (str): Chemin vers le fichier json à lire

        Returns:
            _type_: Contenu du fichier
        """
            
        if os.path.exists(file):
            with open(file, 'r') as f:
                json_content = list(json.load(f))
        
                return json_content
    
    def dns_requests(domain: str):

        """Fait les requêtes vers les serveurs (NS), les srveurs mails (MX), l'admin serveur (SOA), et les third-app (TXT)

        Returns:
            dict: Dictionnaire avec tous les résultats
        """
        if domain != None:

            #NS Record
            try:
                result = dns.resolver.query(domain, 'NS')
                ns_record = [('NS Record : ', val.to_text()) for val in result]

            except:
                ns_record = None

            #MX record
            try:
                result = dns.resolver.query(domain, 'MX')
                mx_record = [('MX Record : ', val.to_text()) for val in result]

            except:
                mx_record = None

            #SOA record
            try:
                result = dns.resolver.query(domain, 'SOA')
                soa_record = [('SOA Record : ', val.to_text()) for val in result]

            except:
                soa_record = None


            #TEXT record
            try :
                result = dns.resolver.query(domain, 'TXT')
                txt_record = [('TXT Record : ', val.to_text()) for val in result]

            except:
                txt_record = None

            return {
                'NS Record' : ns_record,
                'MX Record' : mx_record,
                'SOA Record' : soa_record,
                'TXT Record' : txt_record
            }

class DnsChecker:


    def __init__(self, file_extension, column_name, url_type, sheet_name=None, column_filter=None):

        """Constructeur de la classe 
        """
        
        self.file_extension = file_extension
        self.column_name = column_name
        self.url_type = url_type
        self.column_filters = column_filter
        self.sheet_name = sheet_name
        
        self.DATA_FILE_PATH = f"/home/ec2-user/data/data_file{self.file_extension}"
        self.JSON_FILE_PATH = "/home/ec2-user/data/DNS_results_company.json"
        self.RESULTS_FILE = f"/home/ec2-user/data/dns_checking{self.file_extension}"
        self.DNS_RESULTS_COMPANY = DnsCheckerFunctions.read_json_file(self.JSON_FILE_PATH)
        
        
        self.dict_records = self.DNS_RESULTS_COMPANY[0]
        self.request_keys = self.DNS_RESULTS_COMPANY[1]

        #Télécharge les fichiers et supprime les lignes où il n'y a pas d'url

        if (self.file_extension == ".xlsx") and (self.sheet_name != None):
            
            self.df = pd.read_excel(self.DATA_FILE_PATH, sheet_name=self.sheet_name)
            self.df.dropna(subset=[column_name], inplace=True)
        
        elif self.file_extension == ".csv":

            self.df = pd.read_csv(self.DATA_FILE_PATH)   
            self.df.dropna(subset=[column_name], inplace=True)
        
        else:
            print("ERROR send compatible files")

        #S'il y a un filtre, à chaque fois qu'une valeur est absente dans la colonne filtrée, toute la ligne est supprimée
        if self.column_filters != None:
            self.df.dropna(subset=[self.column_filters], inplace=True)
            self.df.reset_index(drop=True, inplace=True)

    def website_to_domain(self):
        """Convertit un website en nom de domaine
        """
        
        domains = []
        
        for website in list(self.df[self.column_name]):
            if (website != None):
                name = Path(str(website)).name
                
                if name[:4] == "www.":
                    
                    domain = name[4:]
                
                else:
                    domain = name
                
                domains.append(domain)
            else:
                domains.append(None)
        
        self.df['domain'] = domains

    def url_to_domain(self):
        """Convertit un url en nom de domaine
        """
        
        websites = []
        domains = []

        for value in self.df[self.column_name].values:
            if str(value).find(",") != -1:
                res = value.split(',')[0][8:]
                websites.append(res[:res.find('/')])
            else:
                res = str(value)[8:]
                websites.append(res[:res.find('/')])

        for website in websites:
            if (website != None):
                name = Path(str(website)).name
                
                if name[:4] == "www.":
                    
                    domain = name[4:]
                
                else:
                    domain = name
                
                domains.append(domain)
            else:
                domains.append(None)
        
        self.df['domain'] = domains

    
    def dns_response_analysis(self, response: dict):

        """Analyse le résultat d'une requête, transmis sous forme de dictionnaire

        Returns:
            dict: Dictionnaire contenant tous les services liés au nom de domaine
        """
    
        response_analysis = {
            'MX Record' : [],
            'NS Record' : [],
            'SOA Record' : [],
            'TXT Record' : []
        }
        
        #Première boucle qui itère sur ['MX Record', 'NS Record', ....] : les clés du dictionnaire transmis
        for request in self.request_keys.get('request_keys'):
            results = response.get(request)
            #On récupère tous les résultats de 'MX Record' par exemple, sous forme de liste
            if results != None:
                #S'il y a des résultats on itère sur chacun d'eux
                for result in results:
                    
                    #self.dict_records est la liste de tous les services avec la syntaxe à rechercher pour chaque requête, il est dans DNS_results_company.json sur le serveur
                    #On itère sur les clés et les valeurs du dictionnaire
                    for key, value in self.dict_records.items():
                        
                        #S'il existe un marqueur pour le service concerné on va regarder s'il est dans le résultat de la requête
                        if value.get(request) != None:

                            #Si on trouve le marqueur dans le résultat de la requête on ajoute le service à la liste des services trouvés
                            if (result[1].find(value.get(request)) != -1) and (key not in response_analysis.get(request)):
                                response_analysis.get(request).append(key)
                        
                        #Sinon on ajoute rien
                        else:
                            response_analysis.get(request).append(None)
        
        for key in response_analysis:
            response_analysis[key] = ", ".join(response_analysis[key])
        
        return response_analysis
    

    def run(self):
        """Lance l'analyse
        """

        mx = []
        ns = []
        soa = []
        txt = []

        #On fait les conversions nécessaires
        if self.url_type == 'url':
            self.url_to_domain()
        
        elif self.url_type == 'website':
            self.website_to_domain()

        elif self.url_type == 'domain':
            self.df['domain'] = self.df[self.column_name]
        
        #On itère sur chaque nom de domaine de la liste pour faire la requête DNS, la traiter, et l'enregistrer dans une liste
        for domain in self.df['domain'] :

            request_response = DnsCheckerFunctions.dns_requests(domain)
            analysed_response = self.dns_response_analysis(request_response)
        

            mx.append(analysed_response.get('MX Record'))
            ns.append(analysed_response.get('NS Record'))
            soa.append(analysed_response.get('SOA Record'))
            txt.append(analysed_response.get('TXT Record'))
        
        #On ajoute les colonnes récemment trouvées au tableau
        self.df["Mail server"] = mx
        self.df["Host server"] = ns 
        self.df["Admin server"] = soa
        self.df["Third-party app"] = txt

        #On convertit le tableau en fichier excel ou csv dans le même format que le fichier d'origine
        if self.file_extension == '.xlsx':
            self.df.to_excel(self.RESULTS_FILE)
        
        elif self.file_extension == '.csv':
            self.df.to_csv(self.RESULTS_FILE)


if __name__ == '__main__':

    pass