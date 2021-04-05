# Ajouter l'altitude sur des cartes openstreetmap à l'aide d'un modèle numérique de terrain

Ceci s'effectue en executant le script ajout_elevation_avec_mnt.py
Ce script est en développement. 

Ce prend en entrée la carte openstreetmap de La Brossière 
https://www.geoportail.gouv.fr/
la brossière, 85250 Saint-André-Goule-d'Oie

Cette carte est fourni dans ce répertoire, et s'appelle La_brossière.xml

Ce scrit utilise les modèles numériques de terrain libres depuis le 1er janvier 2021
https://geoservices.ign.fr/documentation/diffusion/telechargement-donnees-libres.html
https://geoservices.ign.fr/documentation/diffusion/telechargement-donnees-libres.html#rge-alti-1-m
Comme la route qui nous intéresse est en vendée, les cartes de vendées doivent être téléchargées.
Elles ne sont pas dans le répertoire, car la taille est de l'ordre de 21Go


La sortie du script est la carte openstreetamp La_brossiere_avec_elevation_mnt.xml

