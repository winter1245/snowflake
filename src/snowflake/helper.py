
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
