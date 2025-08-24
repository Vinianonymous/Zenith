def showlist(lis):
    for i in range(len(lis)):
        print(f"List {i+1}: {lis[i]}")
    print()
def sre():  
    dayin = ["Bible + 2 min prayer", "Work out"]
    try:
        print("Press Ctrl+C to stop adding tasks.")
        while True:
            showlist(dayin)
            dayin.append(input("Add: "))
            print("\n")
    except KeyboardInterrupt:
        for i in range(len(dayin)):
         print(f"List {i+1}: {dayin[i]}")
    #engaging execution
    done = 0
    while done != len(dayin):
        showlist(dayin)
        try:
            toi = int(input("Inmediate: "))-1
        except ValueError:
            toi = int(input("Inmediate: "))-1
        done_input = input("Is your task done? y/n ")
        if done_input == "y":
            print(f"Task: {dayin[i]} DONE. Reanchor for 2 minutes and engage another.")
            dayin.remove(dayin[toi])
            done +=1
        else:
            print("Reanchor for 1 minute and reengage")
