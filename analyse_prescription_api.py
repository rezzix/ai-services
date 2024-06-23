import openai
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify 
from apiflask import APIFlask

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

"""
patient = "patient : " + "homme de 25 ans"
case = "cas : " +"fievre et toux sèche"
prescriptor = "prescripteur : " + "Traumatologue"
prescription = "Warfarin 5mg, une fois par jour. Ibuprofen 100mg, toutes les  4 à 6 heures au besoin."
"""
gptversion="gpt-4o"

def analyseGPT(patient, case, prescriptor, prescription, model=gptversion):
    agent = "Tu es medecin travaillant pour une assurance, ta mission est d'évaluer les prescriptions pour le patient présenté et alerter sur les éventuelles intéractions ou risques de fraude (declaration de prescriptions inutiles ou dangereuses). Pour des raisons de confidentialité, tu ne peux pas demander de renseignements supplémentaires sur le patient ou le prescripteur."
    task = "Quelles sont les notifications et alerte par rapport à cette prescription ? donnes des réponses courtes et évites les consigne génériques comme vérifiez avec votre médecin, le prescripteur est supposé avoir déjà vérifié les prescriptions et allérgies. Reponses sous forme de liste de points de quatre catégories : 'risques de fraude', 'prescription dangereuse', 'prescription inutile' ou 'hors spécialité' dans cet ordre. n'affiche pas une catégorie si elle ne s'applique pas et ne répète pas le même problème sous deux catégories différentes."

    messages = [{"role": "system", "content": agent},
              {"role": "user", "content": patient},
              {"role": "user", "content": prescription},
              {"role": "user", "content": prescriptor},
              {"role": "user", "content": task}]
    
    if case and case.strip() :
        messages.append ({"role": "user", "content": case})
    
    client = OpenAI()
    response = client.chat.completions.create(model=model, messages=messages, temperature=0, )
    #return response.choices[0].message["content"]
    print(type(response.choices[0].message))
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def lettreRefusGpt(patient, case, prescriptor, prescription, editor, model=gptversion):
    agent = f"Tu es medecin qui s'appelle {editor}, travaillant pour la mutuelle CNSS à Casablanca, ta mission est d'évaluer les prescriptions pour le patient présenté et alerter sur les éventuelles intéractions ou risques de fraude (declaration de prescriptions inutiles ou dangereuses). Pour des raisons de confidentialité, tu ne peux pas demander de renseignements supplémentaires sur le patient ou le prescripteur."
    task = "Tu dois rédiger une lettre de refus de prise en charge du de prise en charge de la feuille de soin, et expliquer les raisons de refus. donnes des raisons courtes sous forme de liste de points de trois catégories : 'prescription dangereuse', 'prescription inutile' ou 'hors spécialité' dans cet ordre. n'affiche pas une catégorie si elle ne s'applique pas et ne répète pas le même problème sous deux catégories différentes."

    messages = [{"role": "system", "content": agent},
              {"role": "user", "content": patient},
              {"role": "user", "content": prescription},
              {"role": "user", "content": prescriptor},
              {"role": "user", "content": task}]
    
    if case and case.strip() :
        messages.append ({"role": "user", "content": case})
    
    client = OpenAI()
    response = client.chat.completions.create(model=model, messages=messages, temperature=0, )
    #return response.choices[0].message["content"]
    print(type(response.choices[0].message))
    print(response.choices[0].message.content)
    return response.choices[0].message.content


app = APIFlask(__name__)

@app.route("/analyse_prescription", methods=["POST"])
def analyse_prescription():
    """
    Return an analysis for medical prescriptions.
    ---
    responses:
      200:
        description: a list of analysis elements.
        content:
          application/json:
    """
    print("received ", request.get_json())
    data = request.get_json()
    #result = analyseGPT( data["patient"], data["case"], data["prescription"],"gpt-3.5-turbo")
    result = analyseGPT(data["patient"], data["case"], data["prescription"], data["prescriptor"],gptversion)
    print("returning ")
    #return jsonify(result.split("\n\n"))
    return jsonify(result)
    #return result
  

@app.route("/lettre_refus", methods=["POST"])
def lettre_refus():
    """
    Return an letter to justify the refusal of refund for the given prescriptions.
    ---
    responses:
      200:
        description: a list of analysis elements.
        content:
          application/json:
    """
    print("received ", request.get_json())
    data = request.get_json()
    #result = analyseGPT( data["patient"], data["case"], data["prescription"],"gpt-3.5-turbo")
    result = lettreRefusGpt(data["patient"], data["case"], data["prescription"], data["prescriptor"], data["editor"],gptversion)
    print("returning ")
    #return jsonify(result.split("\n\n"))
    return jsonify(result)  
  
@app.cli.command()
def openapi():
    """Generate OpenAPI documentation."""
    from apiflask.core import current_app
    from apiflask.spec import generate_openapi

    spec = generate_openapi(current_app)
    with open('openapi.json', 'w') as f:
        f.write(spec.to_json())

@app.route("/index", methods=["GET"])
def index():
    return "Analyse de prescriptions medicales"
  
if __name__ == "__main__":
  app.run(debug=True)