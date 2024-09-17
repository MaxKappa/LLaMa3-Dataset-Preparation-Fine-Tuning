import json
import random

with open(f'/Users/massimiliano/Desktop/UNIMI/tesi/data/cleanAlpaca/testc.jsonl') as file:
    data = json.load(file)
random.shuffle(data)
with open('/Users/massimiliano/Desktop/UNIMI/tesi/data/cleanAlpaca/testcMixed.jsonl', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Il file è stato mescolato con successo.")
