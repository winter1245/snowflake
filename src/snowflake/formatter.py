import sys

def formatScope():
    
    with open("scope.txt", "rb") as f:
        lineCount = sum(1 for _ in f)

    with open('scope.txt') as scope:
        i=0
        for line in scope:
            i+=1
            sys.stdout.write('\r')
            sys.stdout.write('seperating scope [' + str(i) + ' of ' + str(lineCount) + ']')
            sys.stdout.flush()

            if line[0]=='*':
                wildcard=line[1:] # remove *
                try:
                    with open('wildcard.txt', 'a') as file:
                        file.write(wildcard)

                except OSError:
                    print("Writing to wildcard.txt failed")

            else:
                try:
                    with open('active.txt', 'a') as file:
                        file.write(line)

                except OSError:
                    print("Writing to active.txt failed")


        sys.stdout.write('\n')
        return 
