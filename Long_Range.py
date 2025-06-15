import json

#Dear me of the future, please find out how to use this, for I have lost enoUGH DAMN TIME WITH HEADACHES
def data_handler(operation, dicti):
    with open("data.json"):
        if operation == "read":
            json.loads(dicti)
        elif operation == "write":
            json.dumps(dicti)

def weekin():
    weekdays = {
        "sunday":" ",
        "monday":" ",
        "tuesday":" ",
        "wednesday":" ",
        "thursday":" ",
        "friday":" ",
        "saturday":" "
    }

    for i in weekdays:
        weekdays[i] = input(f"{weekdays[i]} log: ") 
    print("Please, go on to load the habitica and tasks.")
    input("Press enter when done.")

    print("Data dump successfull. Closing Operation.")

