# test file working
import json

array = []

with open("base_data.txt", encoding='utf-8') as f:
    for i in f:
        line = i.lower().split('\n')[0]
        if(line != ''):
            array.append(line)

with open('cenz.json', 'w', encoding='utf-8') as f:
    json.dump(array, f)
