from flask import Flask, request, jsonify, render_template
import openai
import json
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
# Créer un objet OpenAI
openai.api_key = secret_key


@app.route('/', methods=['POST', 'GET'])
def ask_question():
    if request.method == 'POST':
        question = request.form['question']
        print("question:", question)
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"tu est un agent de voyage qui a 8 ans d’expérience dans le  voyage de tourisme pour particulier et qui voyage à moto depuis 5 ans à la recherche de paysage époustouflants ton nom est Edouard CERRA peut tu faire les recommandation de destination en fonction de ce text : {question}.",
            max_tokens=200
        )
        result = response.choices[0].text.strip()

        response1 = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Ecris-moi un JSON inspiré de ce texte : {result}, contenant une liste de toutes les destinations disponibles. Chaque élément de la liste doit être un objet JSON avec une clé 'name' et une valeur contenant le nom du pays. Seule la clée name n'est accepter dans la réponse ! L'ensemble doit être au format JSON.",
            max_tokens=2000
        )

        list = json.loads(response1.choices[0].text.strip())
        print("list:", list)

        return render_template('index.html', result=result, list=list)
    else:
        print("no question")
    return render_template('index.html')


@app.route('/country/<country_name>')
def country_detail(country_name):
    # Récupérez les détails spécifiques du pays à afficher, par exemple à partir d'une base de données ou d'une autre source de données.
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f" j'aimerai avoir un descriptif touristique, avec les information comme le nombre d'habitant, le PIB, pour le pays qui est  : {country_name}, cette reponse doit etre en français.",
        max_tokens=500
    )

    country_name = response.choices[0].text.strip()
    # Ensuite, affichez les détails dans un modèle HTML dédié.
    # Vous pouvez renvoyer un modèle HTML différent pour chaque pays ou un seul modèle avec des détails dynamiques basés sur le pays sélectionné.
    return render_template('country_detail.html', country_name=country_name)


@app.route('/ask', methods=['POST', 'GET'])
def ask_chat():
    if request.method == 'POST':
        question = request.form['question']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"tu es un agent de voyage qui a 8 ans d’expérience dans le voyage de tourisme pour particulier et qui voyage à moto depuis 5 ans à la recherche de paysages époustouflants. Ton nom est Edouard CERRA, tu conseil sur les destinations à travers le monde, à partir de ce text {question} peut tu me conseiller des destinations ?, les réponses doivent être en français.",
            max_tokens=200
        )
        result = response.choices[0].text.strip()
        return jsonify(result=result)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
