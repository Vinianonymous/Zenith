from Short_Range import sre
from timed import timer
from Long_Range import weekin

def main():

    print("Welcome to the engager hub.")
    try:
       while True:
           print("Loop enabled.")
           input("wanna stop? Ctrl c now")
           sre()
    except KeyboardInterrupt:
        print("Loop exited. Program execution ending now. DEUS VULT")

main()