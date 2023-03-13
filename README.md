# Système de prise de rendez-vous automatique en ligne

Ce projet a été réalisé pour répondre aux besoins d'un coach en développement personnel qui souhaitait mettre en place un système de prise de rendez-vous en ligne.  

## Fonctionnalités  

Le projet est composé de deux applications :  

### Usersapp

Cette application gère l'authentification des utilisateurs et les vues associées. Elle comprend les fonctionnalités suivantes :
- une page d'accueil présentant le travail du coach en développement personnel
- un système d'authentification permettant au coach et à ses utilisateurs de se connecter au site, de se déconnecter, de modifier leurs informations et mot de passe.

### Bookingapp

Cette application est dédiée à la prise de rendez-vous et à la gestion des séances passées. Elle offre les fonctionnalités suivantes :
- un système de prise de rendez-vous pour le client avec choix du jour, puis de l'heure et possiblité de préciser le motif du rendez-vous
- une gestion des séances futures du coach :
    - ajout / modification / suppression de notes pour chaque rendez-vous
    - annulation d'un rendez-vous client, et envoi d'un mail d'information
- une gestion des séances futures du client :
    - modification du jour, de l'heure et du motif
    - annulation du rendez-vous
- accès à l'historique des rendez-vous :
    - le coach peut également voir les notes, et les éditer ou supprimer

## Technologies utilisées

Le projet a été réalisé en utilisant le framework Django et le langage de programmation Python.  
Comment lancer le projet ?  

Pour lancer le projet, il faut tout d'abord installer Django et Python, ainsi que les dépendances du projet qui sont listées dans le fichier requirements.txt. Ensuite, cloner le projet à partir du dépôt Github.  
Enfin, exécuter les commandes suivantes :  

pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  

Le projet sera accessible à l'adresse http://localhost:8000/.