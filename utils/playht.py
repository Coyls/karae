import json
import requests

from playsound import playsound

headers = {'Authorization': '0cedff6797b04c4491cefab309ed9fc1',
           'X-User-ID': '7hmdkjbDDORO7sSIAm2w4kiNtmo1', 'Content-Type': 'application/json'}
data = {
    'voice': 'Lea',
    'content': ['Bonjour, la temperature est de 10 degrée et nous somme le 4 mai 2022'],
    'title': 'testapi'

}

# r = requests.post('https://play.ht/api/v1/convert',
#                   json=data, headers=headers)


transcriptionId = '-N1E087RxvYOvgb3GSCK'
r = requests.get(f'https://play.ht/api/v1/articleStatus?transcriptionId={transcriptionId}', headers=headers)

print("Status Code", r.status_code)
print("JSON Response ", r.json())

playsound("https://media.play.ht/full_-N1E087RxvYOvgb3GSCK.mp3")