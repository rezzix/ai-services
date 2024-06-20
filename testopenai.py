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

agent = "Tu es medecin travaillant pour une assurance, ta mission est d'évaluer les prescriptions pour le patient présenté et alerter sur les éventuelles intéractions ou risques de fraude (declaration de prescriptions inutiles ou dangereuses)."
task = "Quelles sont les notifications et alerte par rapport à cette prescription ? éviter les consigne génériques comme vérifiez avec votre médecin, le prescripteur est supposé avoir déjà vérifié les prescriptions et allérgies. Reponses sous forme json en trois catégories : 'prescription dangereuse' , 'prescription inutile' ou 'risques de fraude'"
patient = "patient : " + "homme de 25 ans"
case = "cas : " +"fievre et toux sèche"
prescription = """
Warfarin 5mg, une fois par jour. 
Ibuprofen 100mg, toutes les  4 à 6 heures au besoin.
"""
gptversion="gpt-4o"

def analyseGPT(patient, case, prescription, model=gptversion):
    messages = [{"role": "system", "content": agent},
              {"role": "user", "content": patient},
              {"role": "user", "content": case},
              {"role": "user", "content": prescription},
              {"role": "user", "content": task}]
    client = OpenAI()
    response = client.chat.completions.create(model=model, messages=messages, temperature=0, )
    #return response.choices[0].message["content"]
    print(type(response.choices[0].message))
    print(response.choices[0].message.content)
    return response.choices[0].message.content

"""
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
"""

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
    result = analyseGPT(data["patient"], data["case"], data["prescription"],gptversion)
    print("returning ")
    #return jsonify(result.split("\n\n"))
    return jsonify(result)
    #return result
  
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