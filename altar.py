from filehandler import handler

altar = {
    "pillars":{
    "faith": 0,
    "resolve":0,
    "GodFriend": 0,
    "Righteous thinking":0
    },
    "fire":0
}

pillars = handler("r", altar, "altar.json")
for i in altar[pillars]:
    altar[pillars][i] += int(input(f"Alteration on {i}: "))


#End of all operations: Write the data to it's file.
handler("w", altar, "altar.json")

