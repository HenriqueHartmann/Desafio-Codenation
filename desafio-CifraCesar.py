import requests
import json
import hashlib
from string import ascii_lowercase

def saveData(data):
    with open('answer.json', 'w') as f:
        json.dump(data, f)

def requestData():
    with open('answer.json', 'r') as f:
        return json.load(f)

def dicCesar(key, ascii_lowercase):
    dic = {}
    i = 0
    for position, element in enumerate(ascii_lowercase):
        if position >= (len(ascii_lowercase) - key):
            dic[ascii_lowercase[i]] = element
            i += 1
        else:
            dic[ascii_lowercase[position + key]] = element
    return dic

def decipher(key, message):
    dic = dicCesar(key, ascii_lowercase)
    message = message.lower()
    lista = []
    for letter in message:
        if letter.isalpha():
            lista.append(dic[letter])
        else:
            lista.append(letter)    
    result = ''.join(lista)
    return result

req = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=305c35da2b4716e063c30583caa180fa036e823a')
req = req.json()

saveData(req)
data = requestData()

key = data['numero_casas']
message = data['cifrado']

answer = decipher(key, message)
data['decifrado'] = answer

saveData(data)

data['resumo_criptografico'] = hashlib.sha1(answer.encode(encoding="UTF-8")).hexdigest()

saveData(data)

url_post = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=305c35da2b4716e063c30583caa180fa036e823a'
answer = {'answer': open('answer.json', 'rb')}
req = requests.post(url_post, files=answer)
