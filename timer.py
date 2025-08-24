import time
from mediahandler import playsong
def clock(mode, task):
    if mode == "stopwatch":
        print("T. Mode: Stopwatch")
        timer = {
            "hours": 0,
            "minutes": 0,
            "seconds":0
        }
        try:  
            while True:
                player = playsong
                player.play()
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
        except KeyboardInterrupt:
            print(f"\nTime logged for {task}:\n {timer['hours']:02}:{timer['minutes']:02}:{timer['seconds']:02}") 

