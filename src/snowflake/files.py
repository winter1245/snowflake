import threading
from pathlib import Path
import sys
from time import time,sleep,gmtime,strftime 
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import os
import requests

try:
    from snowflake.params import args
    import snowflake.helper as helper
    import snowflake.wrapper as wrapper
except ImportError:
    from params import args
    import helper
    import wrapper

def probe(timestamp,subdomain):

    alive=[]
    http= 'http://' + subdomain[:-1]
    https = 'https://' + subdomain[:-1]
    path = f'data/{timestamp}/{subdomain[:-1].replace('.','_')}/'
    if not os.path.isdir(path):
        os.makedirs(path)

    try:
        r = requests.get(http,timeout=15)
        alive.append(http + '\n')
        helper.append(f'data/{timestamp}/statuscodes.txt',f'{r.status_code} {http}\n')
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            title=soup.title.string
        except AttributeError:
            title=soup.title
        
        helper.write(f'{path}responsehttp.txt',r.text)
        helper.append(f'data/{timestamp}/titles.txt',f'{title} {https}\n')
        header=''
        for key, value in r.headers.items():
            header += f'{key}: {value}\n'
        helper.write(f'{path}headerhttp.txt',f'{header}')

    except requests.exceptions.RequestException:
        pass

    try:
        r = requests.get(https,timeout=20)
        alive.append(https + '\n')
        helper.append(f'data/{timestamp}/statuscodes.txt',f'{r.status_code} {https}\n')
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            title=soup.title.string
        except AttributeError:
            title=soup.title
        
        helper.write(f'{path}responsehttps.txt',r.text)
        helper.append(f'data/{timestamp}/titles.txt',f'{title} {https}\n')
        header=''
        for key, value in r.headers.items():
            header += f'{key}: {value}\n'
        helper.write(f'{path}headerhttps.txt',f'{header}')
    

    except requests.exceptions.RequestException:  
        pass
         
   

    helper.appendFile('alive.txt',alive)
    return


def screenshot(timestamp):
    
    fl = helper.fromFile('alive.txt')
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    
    for alive in fl:
        
        protocol=alive.split(':')[0]
        subdomain=alive[(alive.find('//')+2):]
        folder =subdomain.replace('.','_')[:-1]
        path = f'data/{timestamp}/{folder}/'
        if not os.path.isdir(path):
            os.makedirs(path)
        try:
            driver.get(alive)

            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            
            try:
                with open(f'{path}source{protocol}.html', 'w') as file:
                    file.write(soup.prettify())

            except OSError:
                print(f"Writing to {path} failed")
            
            driver.save_screenshot(f'{path}screenshot{protocol}.png')

        except WebDriverException:
            print(alive + 'not found')    

        
        sleep(5)
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} screenshot website [{fl.index(alive)+1} of {len(fl)}]')     
            sys.stdout.flush()
    
    driver.quit()
    print()
        
    return

def secret(timestamp):
    

    user=str(Path.home())
    files=os.listdir(f'{user}/.gf/')
    if not os.path.isdir(f'data/{timestamp}/secret/'):
        os.makedirs(f'data/{timestamp}/secret/')
    for file in files:
        name= file.split('.')[0]
        out=wrapper.gf(name) 
        helper.write(f'data/{timestamp}/secret/{name}.txt',out)


    return

def threadfunc(timestamp,fl,i):
    
    for index in range(len(fl)):
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[THREAD{i}]{helper.WHITE} probe subdomain [{index} of {len(fl)}]')     
            sys.stdout.flush()
        if index % 10==i:
            probe(timestamp,fl[index])
            sleep(5)
        

    return

def multiprobe(timestamp,fl):
    
    threadlist=[]
    for i in range(10):
        t = threading.Thread(target=threadfunc,args=(timestamp,fl,i), name='t{i}')
        threadlist.append(t)
        t.start()
    
    for t in threadlist:
        t.join()

    print()

    return


def cycle():
    
    timestamp = int(round(time()))
    date = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    if not os.path.isdir('data'):
        os.makedirs('data')
    
    helper.append('data/timestamp',f'{timestamp} {date}\n')

    fl=helper.fromFile('resolved.txt')
    if args.threading:
        multiprobe(timestamp,fl)
    
    else:
        for subdomain in fl:
            probe(timestamp,subdomain)
            if not args.quiet:
                sys.stdout.write('\r')
                sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} probe subdomain [{fl.index(subdomain)+1} of {len(fl)}]')     
                sys.stdout.flush()
            sleep(2)
    
    screenshot(timestamp)
    secret(timestamp)
    return
