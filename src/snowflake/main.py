from snowflake.formatter import formatScope
import os

def init():
     
   

    print("""
  ____                      __ _       _        
/ ___| _ __   _____      __/ _| | __ _| | _____ 
\\___ \\| '_ \\ / _ \\ \\ /\\ / / |_| |/ _` | |/ / _ \\
 ___) | | | | (_) \\ V  V /|  _| | (_| |   <  __/
|____/|_| |_|\\___/ \\_/\\_/ |_| |_|\\__,_|_|\\_\\___|                                                                                                                                                                                                                                                           
    """)
    
    if not os.path.isfile("scope.txt"):
        print(f"{'\033[93m'}[Warning]{'\033[0m'} scope.txt not found")
    
    if not os.path.isfile("secret.txt"):
        print(f"{'\033[93m'}[Warning]{'\033[0m'} secret.txt not found")



    return 


def controller():
    
    try:
        while 1:

            print("[1] seperate scope")
            print("[0] end")
            print("\r\r")

            userIN=input()
            
            match userIN:
                case "1":
                    formatScope()
                case "0":
                    return

    except KeyboardInterrupt:
        return 0

    return 0


def main():
    
    init()
    controller()

    return 0


if __name__ == "__main__":
    main()
