from snowflake.formatter import formatScope
import os.path
from snowflake.params import args

def init():
     
   

    print("""
  ____                      __ _       _        
/ ___| _ __   _____      __/ _| | __ _| | _____ 
\\___ \\| '_ \\ / _ \\ \\ /\\ / / |_| |/ _` | |/ / _ \\
 ___) | | | | (_) \\ V  V /|  _| | (_| |   <  __/
|____/|_| |_|\\___/ \\_/\\_/ |_| |_|\\__,_|_|\\_\\___|                                                                                                                                                                                                                                                           
    """)
    
    if not os.path.isfile("scope.txt"):
        print(f"{'\033[93m'}[WARNING]{'\033[0m'} scope.txt not found")
    
    if not os.path.isfile("secret.txt"):
        print(f"{'\033[93m'}[WARNING]{'\033[0m'} secret.txt not found")



    return 


def controller():
   
   
    
    if args.scope:
        formatScope()
        return
    if args.all:
        formatScope()
        #...
        return
    


    return 


def main():
    
    init()
    controller()

    return 0


if __name__ == "__main__":
    main()
