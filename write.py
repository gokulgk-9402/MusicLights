import json

d = {
    "status": "on"
}
f = open('data.json', 'w')

json.dump(d, f)

