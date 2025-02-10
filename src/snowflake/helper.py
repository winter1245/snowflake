
def appendFile(path,list):
    
    try:
        with open(path, 'a') as file:
            for item in list:
                file.write(item)

    except OSError:
        print(f"Writing to {path} failed")

    return

def writeFile(path,list):
    
    try:
        with open(path, 'w') as file:
            for item in list:
                file.write(item)

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
    
    writeFile(path,unique)

    return

def removeWildcard(path):
    
    fl=fromFile(path)
    
    for i in range(len(fl)):
        if fl[i][0]  ==  '*':
            fl[i]=fl[i][1:]
        if fl[i][0]  == '.':
            fl[i]=fl[i][1:]
    
    writeFile(path,fl)

    return

def removePort(list):
   
    for i in range(len(list)):
        if ':' in list[i]:
            parslist=list[i].split(':')
            list[i] = parslist[0] + '\n'
    
    return list
