import requests
import httpx
try:
    from snowflake.params import args
except ImportError:
    from params import args

def crtsh(page):
   
    params = {
    'q': page,
    'output': 'json',
    }

    r = requests.get('https://crt.sh/', params=params)
    data=r.json()
    assert type(data) is list
    #dict_keys(['issuer_ca_id', 'issuer_name', 'common_name', 'name_value', 'id', 'entry_timestamp', 'not_before', 'not_after', 'serial_number', 'result_count'])
    try:
        with open('subdomains.txt', 'a') as file:
            for entry in data:
                file.write(entry['name_value']+'\n')
                if args.verbose and not args.quiet:
                    print(entry['name_value'])

    except OSError:
        print("Writing to subdomains.txt failed")

    return 

def wayback(page):
    
    url=f'https://web.archive.org/cdx/search/cdx?url=*.{page}/*&output=json&collapse=urlkey&fl=original&pageSize=100&page=0'
    r = httpx.get(url)
    
    data=r.json()
    try:
        with open('wayback.txt', 'a') as file:
            for entry in data:
                file.write(entry[0]+'\n')
                if args.verbose and not args.quiet:
                    print(entry[0])

    except OSError:
        print("Writing to wayback.txt failed")


    return

def filter():
    
    try:
        f=open('subdomains.txt','r')
        fl = f.readlines()
        f.close()
    
    except OSError:
        print("Reading subdomains.txt failed")
    
    for i in range(len(fl)):
        if fl[i][0]  ==  '*':
            fl[i]=fl[i][1:]
        if fl[i][0]  == '.':
            fl[i]=fl[i][1:]

    unique = sorted(list(set(fl)))
    try:
        open('subdomains.txt', 'w').close() # empty file 
    
    except OSError:
        print("Writing to subdomains.txt failed")
    
    try:
        with open('subdomains.txt', 'a') as file:
            for item in unique:
                file.write(item)
    except OSError:
        print("Writing to subdomains.txt failed")


    return
    

def enumeration():
    try:
        f = open("wildcard.txt","r")
        fl = f.readlines()
        f.close()
        for line in fl:
            line=line[:-1]
            print(f'Fetching subdomains for {line}')
            crtsh(line)
            wayback(line)

    except OSError:
        print("Reading wildcard.txt failed")
     
    filter()
    return

