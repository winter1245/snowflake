from time import sleep
import json
import requests
import threading

try:
    from snowflake.params import args
    from snowflake.helper import writeFile,appendFile,fromFile,removeDuplicate,removeWildcard,removePort
except ImportError:
    from params import args
    from helper import writeFile,appendFile,fromFile,removeDuplicate,removeWildcard,removePort

def crtsh(page):
   
    params = {
    'q': page,
    'output': 'json',
    }

    r = requests.get('https://crt.sh/', params=params)
    data=r.json()
    subdomains=[]
    #dict_keys(['issuer_ca_id', 'issuer_name', 'common_name', 'name_value', 'id', 'entry_timestamp', 'not_before', 'not_after', 'serial_number', 'result_count'])
    for entry in data:
        subdomains.append(entry['name_value']+'\n')
        if args.verbose:
            print('crtsh' + entry['name_value'])
    
    appendFile('subdomains.txt',subdomains)

    sleep(15)
    return 

def wayback(page):
    
    url=f'https://web.archive.org/cdx/search/cdx?url=*.{page}/*&output=json&collapse=urlkey&fl=original&pageSize=100&page=0'
    r = requests.get(url)
    list=[]
    data=r.json()
    for entry in data[1:]: #remove first entry "origin"
        subdomain = entry[0]
        parslist = subdomain.split('/') #filter subdomain
        list.append(parslist[2]+'\n')
        if args.verbose and not args.quiet:
            print('wayback:' + subdomain)
    
    removePort(list) 
    appendFile('subdomains.txt',list)
    return

def commoncrawl(page):
    
    url=f'http://index.commoncrawl.org/CC-MAIN-2025-05-index?url=*.{page}&output=json'
    r = requests.get(url)
    tofile=[]
    list=r.text.split('\n')
    for entry in list[:-1]:
        data = json.loads(entry)
        subdomain = data['url']
        parslist = subdomain.split('/')
        tofile.append(parslist[2]+'\n')
    
    appendFile('subdomains.txt',tofile)
    
    return



    
def th1(fl):
    for line in fl:
        line=line[:-1]
        print(f'{'\033[92m'}[THREAD1]{'\033[0m'}Fetching subdomains for {line}')
        crtsh(line)
    return

def th2(fl):
    for line in fl:
        line=line[:-1]
        print(f'{'\033[92m'}[THREAD2]{'\033[0m'}Fetching subdomains for {line}')
        wayback(line)
    return

def th3(fl):
    for line in fl:
        line=line[:-1]
        print(f'{'\033[92m'}[THREAD3]{'\033[0m'}Fetching subdomains for {line}')
        commoncrawl(line)
    return


def enumeration():
   
    fl=fromFile('wildcard.txt')

    if args.threading:
        t1 = threading.Thread(target=th1,args=(fl,), name='t1')
        t2 = threading.Thread(target=th2,args=(fl,), name='t2')
        t3 = threading.Thread(target=th3,args=(fl,), name='t3')
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
    
    else:
        for line in fl:
            line=line[:-1]
            print(f'Fetching subdomains for {line}')
            crtsh(line)
            wayback(line)
            commoncrawl(line)
    
    removeWildcard('subdomains.txt')
    removeDuplicate('subdomains.txt')

    return

