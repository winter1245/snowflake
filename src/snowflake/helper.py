
def toFile(path,list):
    
    try:
        with open(path, 'a') as file:
            for item in list:
               file.write(item + '\n')

    except OSError:
        print(f"Writing to {path} failed")

    return

def fromFile(path):
    
    list = []
    try:
        with open(path, 'r') as file:
            for line in file:
                list.append(line)

    except OSError:
        print(f"Reading {path} failed")


    return list

def removeDuplicate(path):
    
    fl=fromFile(path)

    unique = sorted(list(set(fl)))
    try:
        open(path, 'w').close() # empty file 
    
    except OSError:
        print(f"Writing to {path} failed")
    
    toFile(path,unique)

    return

def removeWildcard(path):
    
    fl=fromFile(path)
    
    for i in range(len(fl)):
        if fl[i][0]  ==  '*':
            fl[i]=fl[i][1:]
        if fl[i][0]  == '.':
            fl[i]=fl[i][1:]
    
    toFile(path,fl)

    return
