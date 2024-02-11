import sys

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json

def tokenize(text):
    stop_words_french = set(stopwords.words('french'))
    tokens = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words_french]
    return tokens

def extraire_urls_positions_et_compter_OU(dictionnaire, tokens_a_garder):
    # Créer un dictionnaire pour stocker temporairement les positions par URL
    positions_par_url = {}

    # Parcourir chaque clé (token) et sa valeur dans le dictionnaire
    for token, infos in dictionnaire.items():
        # Vérifier si le token est dans la liste des tokens à garder
        if token in tokens_a_garder:
            # Pour chaque URL, ajouter les positions au dictionnaire positions_par_url
            urls = infos["urls"]
            positions = infos["positions"]

            for i, url in enumerate(urls):
                if url in positions_par_url:
                    positions_par_url[url].append(positions[i])
                else:
                    positions_par_url[url] = [positions[i]]

    # Créer la liste résultante avec une seule liste par URL
    resultats_filtres = [[url, positions_par_url[url], len(positions_par_url[url])] for url in positions_par_url]

    return resultats_filtres

def extraire_urls_positions_et_compter_ET(dictionnaire, tokens_a_garder):
    # Créer un dictionnaire pour stocker temporairement les positions par URL
    positions_par_url = {}

    # Initialiser un ensemble pour stocker les URLs qui correspondent à tous les tokens à garder
    urls_intersection = set()

    # Parcourir chaque clé (token) et sa valeur dans le dictionnaire
    for token, infos in dictionnaire.items():
        # Vérifier si le token est dans la liste des tokens à garder
        if token in tokens_a_garder:
            # Pour chaque URL, ajouter les positions au dictionnaire positions_par_url
            urls = infos["urls"]
            positions = infos["positions"]

            if not urls_intersection:
                urls_intersection.update(urls)
            else:
                urls_intersection.intersection_update(urls)

            for i, url in enumerate(urls):
                if url in positions_par_url:
                    positions_par_url[url].append(positions[i])
                else:
                    positions_par_url[url] = [positions[i]]

    # Filtrer les URLs qui correspondent à tous les tokens à garder
    urls_intersection = list(urls_intersection)
    resultats_filtres = [[url, positions_par_url[url], len(positions_par_url[url])] for url in urls_intersection]

    return resultats_filtres

def main():
    # Vérifiez s'il y a un unique argument
    if len(sys.argv) == 2:
        print("Veuillez fournir deux arguments après le main.py !")
    else:
        with open('crawled_urls.json', 'r', encoding='utf-8') as file:
            crawled_urls = json.load(file)
        # Créer un dictionnaire pour accéder rapidement aux titres par URL
        dictionnaire_urls_titres = {objet["url"]: objet["title"] for objet in crawled_urls}

        # Récupérez l'argument
        argument = sys.argv[1]
        argument2 = sys.argv[2]

        with open('title.pos_index.json', 'r', encoding='utf-8') as file:
            title_json = json.load(file)

        tokens_a_garder = tokenize(argument)

        if argument2 == 'ET':
            resultat = extraire_urls_positions_et_compter_ET(title_json, tokens_a_garder)
        elif argument2 == 'OU':
            resultat = extraire_urls_positions_et_compter_OU(title_json, tokens_a_garder)
        else:
            print("Le deuxième argument doit être un ET ou un OU")
        
        if resultat:
            resultat = sorted(resultat, key=lambda x: x[2], reverse=True)
            resultat_final = []
            for index, sous_liste in enumerate(resultat, start=1):
                url = sous_liste[0]
                count = sous_liste[2]

                element_dictionnaire = {
                    "rang": index,
                    "url": url,
                    "title": dictionnaire_urls_titres.get(url),
                    "count": count,
                    # Ajoutez d'autres clés en fonction de vos besoins
                }

                resultat_final.append(element_dictionnaire)

        with open('results.json', 'w', encoding='utf-8') as file:
            json.dump(resultat_final, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
