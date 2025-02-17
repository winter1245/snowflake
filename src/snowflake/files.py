from pathlib import Path
import sys
from time import time,sleep,gmtime,strftime 
from selenium import webdriver
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

def probe(timestamp):

    fl= helper.fromFile('resolved.txt')
    alive=[]
    for subdomain in fl:
        
        http= 'http://' + subdomain[:-1]
        https = 'https://' + subdomain[:-1]
        path = f'data/{subdomain[:-1].replace('.','_')}/{timestamp}/'
        if not os.path.isdir(path):
            os.makedirs(path)

        try:
            r = requests.get(http,timeout=20)
            alive.append(http + '\n')
            helper.append('data/statuscodes.txt',f'{r.status_code} {http}\n')
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                title=soup.title.string
            except AttributeError:
                title=soup.title
            helper.append('data/titles.txt',f'{title} {https}\n')
            header=''
            for key, value in r.headers.items():
                header += f'{key}: {value}\n'
            helper.write(f'{path}headerhttps.txt',f'{header}')

        except requests.exceptions.HTTPError:
            print ("Http Error")
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
        except requests.exceptions.Timeout:
            print ("Timeout Error")
        except requests.exceptions.RequestException:
            print ("Other Error")

        try:
            r = requests.get(https,timeout=20)
            alive.append(https + '\n')
            helper.append('data/statuscodes.txt',f'{r.status_code} {https}\n')
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                title=soup.title.string
            except AttributeError:
                title=soup.title
            helper.append('data/titles.txt',f'{title} {https}\n')
            header=''
            for key, value in r.headers.items():
                header += f'{key}: {value}\n'
            helper.write(f'{path}headerhttp.txt',f'{header}')
    

        except requests.exceptions.RequestException:  
            pass
         
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} probe subdomain [{fl.index(subdomain)+1} of {len(fl)}]')     
            sys.stdout.flush()
        sleep(2)

    helper.appendFile('alive.txt',alive)
    print()
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
        path = f'data/{folder}/{timestamp}/'
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

        except selenium.common.exceptions.WebDriverException:
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
    if not os.path.isdir(f'data/secret/{timestamp}'):
        os.makedirs(f'data/secret/{timestamp}')
    for file in files:
        name= file.split('.')[0]
        out=wrapper.gf(name) 
        helper.write(f'data/secret/{timestamp}/{name}.txt',out)


    return



def cycle():
    
    timestamp = int(round(time()))
    date = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    if not os.path.isdir('data'):
        os.makedirs('data')
    try:
        with open(f'data/timestamp.txt', 'a') as file:
            file.write(f'{timestamp} {date}\n')

    except OSError:
                print(f"Writing to data/timestamp.txt failed")


    probe(timestamp)
    screenshot(timestamp)
    secret(timestamp)
    return
