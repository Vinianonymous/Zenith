import time, random, vlc, os

def selectsong():

  
    print("RANDOM audio player engaged successfully.")
    os.chdir('./media/')
    files = os.listdir()
    select = files[random.randint(0,len(files)-1)]
    return select

def timer(mode, task):
    if mode == "stopwatch":
        print("T. Mode: Stopwatch")
        
        timer = {
            "hours": 0,
            "minutes": 0,
            "seconds":0
        }
        
        try:  
            player = vlc.MediaPlayer(selectsong())
            player.play()
            while True: 
                #Timer section
                print(f"{timer['hours']:02}:{timer['minutes']:02}:{timer['seconds']:02}  ", end="\r", flush=True)
                time.sleep(1)
                timer["seconds"] +=1

                if timer["seconds"] == 60:
                    timer["minutes"] +=1
                    timer["seconds"] = 0
                
                if timer["minutes"] == 60:
                    timer["hours"] +=1
                    timer["minutes"] = 0

                #Music
                state = player.get_state()
                if state == vlc.State.Playing or state == vlc.State.Buffering or state == vlc.State.Opening:
                    pass
                elif state == vlc.State.Ended:
                    print("Playback ended.")
                    break
                elif state == vlc.State.Error:
                    print("Error occurred while playing audio.")
                    break
                else:
                        print(f"Waiting... Current state: {state}")
                time.sleep(0.5)

        except KeyboardInterrupt:
            print(f"\nTime logged for {task}:\n {timer['hours']:02}:{timer['minutes']:02}:{timer['seconds']:02}") 

    elif mode == "countdown":
        tos = input("How much time? MM:SS").split(":")
        timer["minutes"] = tos[0]
        timer["seconds"] = tos[1]

        while timer["minutes"] >= 0 or timer["seconds"] >=0:
            print(f"{timer['minutes']:02}:{timer['seconds']:02}", end="\r", flush=True)
            time.sleep(1)

            timer["seconds"] -=1

            if timer['seconds'] == 0 and timer['minutes'] >= 0:
                timer['seconds'] = 59
                timer['minutes'] -=1
            