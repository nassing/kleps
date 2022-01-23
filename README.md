# Kleps
Kleps est un projet étudiant consistant en un réseau social sous forme de messages audio.
Il a été réalisé dans le cadre du projet de fin du premier semestre de première année d'école d'ingénieur et a été développé par :
- [ASSING Norman](https://github.com/nassing) (Chef de projet)
- COUCHEVELLOU Clément
- COUVRAT--PAILLE Titouan
- SEDEKI Khalyl

_Kleps is targeted to French municipalites, thus the project was made in French and did not get an English translation.
If you are still interested in discovering this project, [click here](https://github.com/kleps/edit/main/README_EN.md) to read the English version of this README._

## Démo
Vous pouvez voir [une démonstration de Kleps ici](https://kleps.pythonanywhere.com).
Notez cependant que ce site a été hébergé sur [PythonAnywhere](https://pythonanywhere.com), qui ne permet pas de télécharger des fichiers sur le site. Vous ne pourrez donc pas publier de messages audio.

## Fonctionnalités
- Système de compte : création de compte, connexion, vérification des contraintes
- Messages audio : recording du message, téléchargement sur le serveur, possibilité de faire écouter le message à l'utilisateur, possibilité de donner un titre au message
- Débats : Création, affichage de tous les débats, affichage des propositions de chacun des débats, tri par récence et popularité
- Fonctionnalités contraintes par la connexion: "publier un commentaire ou une proposition" réservé aux utilisateurs connectés, "créer un débat" réservé aux administrateurs
- Possibilité de répondre à un commentaire
- Possibilité de citer une proposition pour en construire une nouvelle
- Statistiques : nombre de jetons utilisés sur chaque débat et chaque proposition, nombre de propositions qui en ont cité une autre, nombre de commentaires pour chaque proposition
- Pages Contact et À propos

## Installation
En l'état, Kleps n'a été utilisé qu'en serveur local, et cette partie détaillera donc la manière de mettre en place ce serveur localement uniquement. Pour héberger le site en ligne, veuillez consulter [la documentation de Flask](https://flask.palletsprojects.com/en/2.0.x/deploying/).
Si ce n'est pas déjà fait, installez [Python 3.10](https://www.python.org/downloads/) (ou une version ultérieure) pour votre système d'exploitation.
Installez ensuite la bibliothèque Flask via cette ligne de commande :
```
$ pip install flask
```
Il ne vous reste plus qu'à cloner ce projet et exécuter ```flask_serv.bat``` si vous êtes sur Windows et ```flask_serv.sh``` si vous êtes sur Linux. Le site sera disponible à l'adresse ```127.0.0.1:5000```

## Contact
Vous pouvez contacter les membres du projet aux adresses mail suivantes :
- Norman : [norman.assing@hotmail.com](mailto:norman.assing@hotmail.com)
- Clément :
- Titouan :
- Khalyl :

## Contribution
Ce dépôt GitHub a davantage l'objectif de mettre en avant les connaissances de l'équipe à ce moment de leur cursus plutôt que de créer une solution complète. Cependant vous êtes libres de récupérer le code source et de le modifier tant que vous respectez la licence ci-dessous.

## Licence
Ce projet est soumis à la licence Apache 2.0
Les principales conditions exigent la préservation du droit d'auteur et de la licence. Les contributeurs doivent fournir une concession expresse des droits de brevet. Les œuvres sous licence, les modifications et les œuvres plus importantes peuvent être distribuées sous différentes conditions et sans code source.
