import ollama
import time

agent = "Tu es medecin travaillant pour une assurance, ta mission est d'évaluer les prescriptions pour le patient présenté et alerter sur les éventuelles intéractions ou risques de fraude (declaration de prescriptions inutiles ou dangereuses). Pour des raisons de confidentialité, tu ne peux pas demander de renseignements supplémentaires sur le patient ou le prescripteur. "
task = "Quelles sont les notifications et alerte par rapport à cette prescription ? donnes des réponses courtes et évites les consigne génériques comme vérifiez avec votre médecin, le prescripteur est supposé avoir déjà vérifié les prescriptions et allérgies. Reponses sous forme de liste de points de quatre catégories : 'risques de fraude', 'prescription dangereuse', 'prescription inutile' ou 'hors spécialité' dans cet ordre. n'affiche pas une catégorie si elle ne s'applique pas et ne répète pas le même problème sous deux catégories différentes. "

patient = "patient : " + "homme de 25 ans. "
case = "cas : " +"fievre et toux sèche. "
prescriptor = "prescripteur : " + "Traumatologue. "
prescription = "prescription : Warfarin 5mg, une fois par jour. Ibuprofen 100mg, toutes les  4 à 6 heures au besoin."

model='mistral-nemo' #'gemma2' 'gemma2:27b' 'ollama3.1'

stream=False
start_time = time.time()

response = ollama.chat(model=model, messages=[
  {
    'role': 'user',
    'content': agent,
  },
  {
    'role': 'user',
    'content': task,
  },
  {
    'role': 'user',
    'content': patient,
  },
  {
    'role': 'user',
    'content': case,
  },
  {
    'role': 'user',
    'content': prescriptor,
  },
  {
    'role': 'user',
    'content': prescription,
  },
  
],
stream = stream,
#format = 'json',
)

if stream :
  for message in response:
    print(message["message"]["content"], end="", flush=True)
else :
  print(response['message']['content'])


elapsed_time = time.time() - start_time
print(f"\nTime taken with {model} model : {elapsed_time:.2f} seconds")

"""
# Stream the response
"""