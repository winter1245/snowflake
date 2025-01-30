
def formatScope():
    
    with open('scope.txt') as scope:
        for line in scope:
            
            if line[0]=='*':
                wildcard=line[1:] # remove *
                with open('wildcard.txt', 'w') as file:
                    try:
                        file.write(wildcard)

                    except:
                        print("writing to file failed")
