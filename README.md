# Ranking

Une expansion de requête et ranking réalisé par Thibaut WOJDACKI

## Comment faire fonctionner l'outil ?

Première étape : Aller dans le bon dossier `cd ranking`

Deuxième étape  : Installer les packages nécessaires - `pip install -r requirements.txt`

Troisième étape : Lancer l'application  `python main.py arg1 arg2`
    où arg1 est la requête de l'utilisateur entre ""
    et arg2 et le mode de requête "ET" ou "OU"

## Fonctionnalités de l'index

L'outil utilise les fichiers crawled_urls.json, title.pos_index.json. Il peut être adapté avec le content.pos_index.json facilement.

Il lit une requête de l'utilisateur en arg1, et la tokenise avec le même algorithme que pour le tp2.

Il filtre ensuite les documents qui ont :
- soit tous les tokens de la requête avec l'arg2 = "ET" 
- soit au moins un token de la requête avec l'arg2 = "OU"