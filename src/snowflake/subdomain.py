from time import sleep
import json
import requests
import threading

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

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
    
    helper.appendFile('subdomains.txt',subdomains)

    sleep(30)
    return 

def wayback(page):
    
    url=f'https://web.archive.org/cdx/search/cdx?url=*.{page}/*&output=json&collapse=urlkey&fl=original&pageSize=100&page=0'
    r = requests.get(url)
    list=[]
    urls=[]
    data=r.json()
    for entry in data[1:]: #remove first entry "origin"
        urls.append(entry)
        subdomain = entry[0]
        parslist = subdomain.split('/') #filter subdomain
        list.append(parslist[2]+'\n')
        if args.verbose and not args.quiet:
            print('wayback:' + subdomain)
    
    helper.removePort(list) 
    helper.appendFile('subdomains.txt',list)
    #helper.appendFile('urls.txt',urls)
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
    
    helper.appendFile('subdomains.txt',tofile)
    
    return

def alienvault(page):
    
    tofile=[]
    url=f'https://otx.alienvault.com/api/v1/indicators/domain/{page}/url_list?limit=100&page=1'
    r = requests.get(url)
    data=r.json()
    list=data['url_list']
    for item in list:
        tofile.append(item['hostname'] + '\n')
        if args.verbose:
            print('alienvault:' + item['hostname'])

    helper.appendFile('subdomains.txt',tofile)
    return


def urlscan(page):
   
    resultlist=[]
    url=f'https://urlscan.io/api/v1/search/?q=domain:{page}'
    r = requests.get(url)
    data=r.json()
    idlist=[]
    #dict_keys(['results', 'total', 'took', 'has_more'])
    for item in data['results']:
        #dict_keys(['submitter', 'task', 'stats', 'page', '_id', '_score', 'sort', 'result', 'screenshot'])
        #dict_keys(['country', 'server', 'redirected', 'ip', 'mimeType', 'url', 'tlsValidDays', 'tlsAgeDays', 'ptr', 'tlsValidFrom', 'domain', 'apexDomain', 'asnname', 'asn', 'tlsIssuer', 'status'])
        if item['page']['apexDomain']==page :
            idlist.append(item['_id'])
    
    for id in idlist:
        sleep(10)
        url=f'https://urlscan.io/api/v1/result/{id}/'
        r = requests.get(url)
        data=r.json()
        #dict_keys(['data', 'lists', 'meta', 'page', 'scanner', 'stats', 'submitter', 'task', 'verdicts'])
        ##dict_keys(['requests', 'cookies', 'console', 'links', 'timing', 'globals'])
        #dict_keys(['ips', 'countries', 'asns', 'domains', 'servers', 'urls', 'linkDomains', 'certificates', 'hashes']) 
        for entry in data['lists']['domains']:
            if entry.endswith(page):
                resultlist.append(entry + '\n')
        
    helper.appendFile('subdomains.txt',resultlist)
    return




    
def th1(fl):
    for line in fl:
        line=line[:-1]
        print(f'{helper.GREEN}[THREAD1]{helper.WHITE}Fetching subdomains for {line} from crtsh')
        crtsh(line)
    return

def th2(fl):
    for line in fl:
        line=line[:-1]
        print(f'{helper.GREEN}[THREAD2]{helper.WHITE}Fetching subdomains for {line} from wayback')
        wayback(line)
    return

def th3(fl):
    for line in fl:
        line=line[:-1]
        print(f'{helper.GREEN}[THREAD3]{helper.WHITE}Fetching subdomains for {line} from commoncrawl')
        commoncrawl(line)
    return

def th4(fl):
    for line in fl:
        line=line[:-1]
        print(f'{helper.GREEN}[THREAD4]{helper.WHITE}Fetching subdomains for {line} from alienvault')
        alienvault(line)
    return


def th5(fl):
    for line in fl:
        line=line[:-1]
        print(f'{helper.GREEN}[THREAD5]{helper.WHITE}Fetching subdomains for {line} from urlscan')
        urlscan(line)
    return


def enumeration():
   
    fl=helper.fromFile('domains.txt')

    if args.threading:
        t1 = threading.Thread(target=th1,args=(fl,), name='t1')
        t2 = threading.Thread(target=th2,args=(fl,), name='t2')
        t3 = threading.Thread(target=th3,args=(fl,), name='t3')
        t4 = threading.Thread(target=th4,args=(fl,), name='t4')
        t5 = threading.Thread(target=th5,args=(fl,), name='t5')
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
    
    else:
        for line in fl:
            line=line[:-1]
            print(f'Fetching subdomains for {line}')
            crtsh(line)
            wayback(line)
            commoncrawl(line)
            alienvault(line)
            urlscan(line)
    
    helper.removeWildcard('subdomains.txt')
    helper.removeDuplicate('subdomains.txt')

    return

