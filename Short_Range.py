from timed import timer
from Long_Range import weekin
from mediahandler import handle


def sre():   
    dayin = ["Bible + 2 min prayer", "Work out"]
    for i in range(len(dayin)):
        print(f"List {i+1}: {dayin[i]}")

    try:
        print("Entering the add loop. Press Ctrl+C to stop adding tasks.")
        while True:
            for i in range(len(dayin)):
                print(f"List {i+1}: {dayin[i]}")
            print("\n")
            dayin.append(input("Add: "))
            print("\n")
    except KeyboardInterrupt:
        for i in range(len(dayin)):
         print(f"List {i+1}: {dayin[i]}")
         
    if "weekin" in dayin:
        print("Long Range detection prompt noticed, engaging week interface.")
        weekin()
    
    #engaging execution

    done = len(dayin)
    while done > 0:
        for i in range(len(dayin)):
            print(f"List {i+1}: {dayin[i]}")

        print("")
        try:
            toi = int(input("Inmediate: "))-1
        except ValueError:
            toi = int(input("Inmediate: "))-1

        timer("stopwatch", dayin[toi])
        done_input = input("Is your task done? y/n ")
        if done_input == "y":
            print(f"Task: {dayin[i]} DONE. Reanchor for 2 minutes and engage another.")
            dayin.remove(dayin[toi])
            done -=1
        else:
            print("Huh? Task not finished after all this time? Reanchor for 1 minute and reengage")

