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
                with open('wildcard.txt', 'a') as file:
                    try:
                        file.write(wildcard)

                    except:
                        print("writing to file failed")

            else:
                with open('active.txt', 'a') as file:
                    try:
                        file.write(line)

                    except:
                        print("writing to file failed")


        sys.stdout.write('\n')
        return 0
