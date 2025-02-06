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
        f = open("wildcard.txt","r")
        fl = f.readlines()
        f.close()
    
    except OSError:
        print("Reading wildcard.txt failed")

    for entry in data:
        fl.append(entry['name_value'])
 

    unique = list(set(fl))
                
    try:
        with open('subdomains.txt', 'a') as file:
            for line in unique:
                file.write(line)
                if args.verbose and not args.quiet:
                    print(line)

    except OSError:
        print("Writing to subdomains.txt failed")

    return 

                
def enumeration():
    try:
        f = open("wildcard.txt","r")
        fl = f.readlines()
        f.close()
        for line in fl:
            crtsh(line)

    except OSError:
        print("Reading wildcard.txt failed")
    
    return

