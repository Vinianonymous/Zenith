import json

pack = {
    "pillars": {
    "faith": 0,
    "resolve":0,
    "GodFriend": 0,
    "Righteous thinking":0
    },
    "fire":0
}

def handler(op, data, fp):
    with open(fp, op) as file:
        match(op):
            case "r":
                return json.load(file)
            case "w":
                json.dump(data, file)

handler("w", pack, "alda.json")
