# Elba_dns_checker

Le projet DNS_checker est un projet d'OSINT permettant de faire des requêtes sur des noms de domaine et de traiter les réponses pour avoir une idée claire des outils utilisés par une entreprise.

Le projet a une composante utilisateur et une composante serveur : 
L'utilisateur dispose d'une interface graphique (GUI) pour rentrer toutes les informations nécessaires au traitement de sa requête qui est ensuite exécutée sur un serveur pour gagner du temps


Il récupère ensuite les résultats sous la forme d'un fichier excel ou csv.

La page d'accueil est la suivante :

![page d'acceuil](https://user-images.githubusercontent.com/59396030/181507957-6cddab98-0996-48e3-aff2-b762a783b95c.png)

Les informations du serveur actuellement utilisé sont les suivantes :

hostname : ec2-44-202-230-6.compute-1.amazonaws.com
username : ec2-user


Après l'installation de l'app comme pour changer de serveur, il faut la reconfigurer.
Pour cela cliquez sur "Config app"

![Menu de configuration](https://user-images.githubusercontent.com/59396030/181508108-67e8ab43-cdc5-498a-8929-67c9b187a374.png)

Puis cliquez sur "Set up a server" et tapez le nom d'utilisateur du serveur :

![setup username](https://user-images.githubusercontent.com/59396030/181508512-e3e4b92d-abf8-4701-9728-22e4ca7a4b2b.png)

Puis rentrez le nom d'hôte :

![set up hostname](https://user-images.githubusercontent.com/59396030/181508583-3b3a572c-59e6-48a4-8e63-caee43b10dad.png)

Enfin, vous devrez indiquer le chemin vers votre clé de connexion

![set up key](https://user-images.githubusercontent.com/59396030/181508698-f293d2f4-e3bc-4e94-9dae-6440e07a41d9.png)

Si l'application était déjà configurée, cette action supprime le mot de passe déjà enregistré il faut donc l'enregistrer une nouvelle fois. Si c'est la première fois que vous configurez l'application, vous devez également renseigner votre mot de passe dans "Configure your password" :

![config password](https://user-images.githubusercontent.com/59396030/181509375-d2ce8cd9-c405-499b-93d5-e98c54d91afe.png)

Après cette étape, vous êtes prêts à démarrer, mais avant cela vérifiez que les changements ont bien été pris en compte, cliquez sur "Server info" dans le menu de configuration 

![server info](https://user-images.githubusercontent.com/59396030/181509693-bb82fdfc-1e8e-4c88-b205-b8ea22484513.png)

Si toutes les informations que vous avez renseignées s'y trouvent bien, excepté le mot de passe qui est chiffré, vous pouvez commencer.

Cependant, il existe d'autres options dans le menu de configuration comme "Compare passwords" qui vous permet de vérifier si le mot de passe que vous vous apprêtez à taper est correct 

![compare password](https://user-images.githubusercontent.com/59396030/181510238-f945d7a6-0263-4eea-b580-9e6bfe958831.png)

Enfin, vous pouvez changer de clé pour le serveur déjà enregistré avec "Load key"


Lancer une analyse :

Rendez-vous sur la page d'accueil :

![page d'acceuil](https://user-images.githubusercontent.com/59396030/181510828-89811d51-65d9-4b65-8438-3b15bcf589ca.png)

Choisissez un fichier csv ou excel (dans cet exemple, c'est un csv)

![select file csv](https://user-images.githubusercontent.com/59396030/181511001-a113cfa2-39ec-4213-9b12-38fcfda4b20a.png)

Puis sélectionner la colonne dans laquelle chercher les urls :
Si le fichier sélectionné est un fichier .xlsx vous devrez d'abord choisir quelle feuille utiliser

![select col csv](https://user-images.githubusercontent.com/59396030/181511127-8451a0e8-d397-4fb4-bc26-d68ee2d393c1.png)

Vous pouvez également sélectionner une colonne à filtrer, c'est-à-dire que pour toute valeur manquante dans la colonne sélectionnée, toute la ligne est supprimée.

![select filter csv](https://user-images.githubusercontent.com/59396030/181511350-38676466-8f58-4244-8a77-ac15d9d67b97.png)

Choisissez ensuite le type d'url que vous voulez traiter :

-URL : https://www.elba.security/

-WEBSITE : www.elba.security

-DOMAIN : elba.security


![select url csv](https://user-images.githubusercontent.com/59396030/181511464-778227da-33de-4303-89b6-6ab67531f2a1.png)

Puis indiquez l'endroit où vous voulez enregistrer le fichier contenant les résultats

![save as csv](https://user-images.githubusercontent.com/59396030/181512208-d70763ac-9f86-4fe9-b7a4-c74523ce5d21.png)

Enfin, entrez le mot de passe de la clé et cliquez sur "Lancer l'analyse"

![lancer l'analyse](https://user-images.githubusercontent.com/59396030/181511683-b5e9609d-99da-45ba-8d2a-0ec937350480.png)

Une fois l'analyse terminée, une dernière fenêtre s'ouvre pour vous rappeler l'endroit où est enregistré le fichier, le temps d'exécution et les erreurs s'il y en a eu

![results](https://user-images.githubusercontent.com/59396030/181512081-5ee06284-3e93-4608-905f-6840e96094f1.png)


ATTENTION : 

-Seules les clés de connexion OpenSSh (.pem) sont prises en charge par l'application 

-Vous devez enregistrer le fichier de résultats sous le même format que le fichier de départ

-Si le fichier est endomagé, l'analyse peut ne pas fonctionner 

Par exemple un téléchargement depuis google drive peut causer des problèmes donc si l'analyse ne fonctionne pas, ouvrez le fichier téléchargé depuis google drive et "réparez" le à l'aide des outils excel avant de réessayer.


Pour se connecter au server via PuTTy :

Host Name : ec2-user@ec2-44-202-230-6.compute-1.amazonaws.com

Vérifiez que le port sélectionné est bien le port 22 

Vérifiez que SSH est bien coché dans "Connection type"

![putty home](https://user-images.githubusercontent.com/59396030/181573452-78750b60-3438-4133-8702-38b10fa37469.png)

Puis allez dans l'onglet Category et Connection/SSH/Auth

Et indiquez la clé de connexion dans "Private key file for authentication"

![putty auth](https://user-images.githubusercontent.com/59396030/181573499-2f1ce014-cf10-4aec-8403-be82ebfa85b3.png)

Il faut une clé Putty c'est-à-dire une clé dont l'extension est ".pkk". Si vous n'avez qu'une clé OpenSSh, dont l'extension est ".pem" il faut la convertir au format ".pkk" avec l'outil "PuTTygen" fournit par PuTTy

![puttygen app](https://user-images.githubusercontent.com/59396030/181573549-4abdafe3-6f9f-4637-9aa7-3e188d3566ad.png)

Importez votre clé :

![import key](https://user-images.githubusercontent.com/59396030/181575691-76134627-6bed-499f-b6bc-41e832eaefe6.png)

Enregistrez la clé privée :

![save private key](https://user-images.githubusercontent.com/59396030/181575773-4745b34a-923a-442d-a168-bb07c82df277.png)

Pour faire la conversion dans l'autre sens, chargez la clé :

![load key](https://user-images.githubusercontent.com/59396030/181576154-05b3467a-a2d9-4a6e-9141-e5c434200980.png)

Exportez la clé au format OpenSSH

![export openssh key](https://user-images.githubusercontent.com/59396030/181576242-93183d1e-c8e1-453e-a448-1387ccc3b708.png)



