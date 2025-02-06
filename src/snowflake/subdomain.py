import requests
from snowflake.params import args

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
                file.write(entry['name_value'])
                if args.verbose and not args.quiet:
                    print('name_value')

    except OSError:
        print("Writing to subdomains.txt failed")

    return 

def filter():
    
    try:
        f=open('subdomains.txt','r')
        fl = f.readlines()
        f.close()
    
    except OSError:
        print("Reading wildcard.txt failed")

    unique = list(set(fl))
    try:
        open('subdomains.txt', 'w').close() # empty file 
    
    except OSError:
        print("Reading wildcard.txt failed")
    
    try:
        with open('subdomains.txt', 'a') as file:
            for item in unique:
                file.write(item)
    except OSError:
        print("Reading wildcard.txt failed")


    return
    

def enumeration():
    try:
        with open("wildcard.txt","r") as f:
            for line in f:
                crtsh(line)

    except OSError:
        print("Reading wildcard.txt failed")
   
    filter()
    return

