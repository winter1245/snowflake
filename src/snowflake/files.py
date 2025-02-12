import sys
from time import time,sleep,gmtime,strftime 
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import requests

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

def probe():

    fl= helper.fromFile('resolved.txt')
    alive=[]
    for subdomain in fl:
        
        http= 'http://' + subdomain[:-1]
        https = 'https://' + subdomain[:-1]

        try:
            r = requests.get(http)
             
            alive.append(http + '\n')
    

        except requests.exceptions.HTTPError:
            print ("Http Error")
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
        except requests.exceptions.Timeout:
            print ("Timeout Error")
        except requests.exceptions.RequestException:
            print ("Other Error")

        try:
            r = requests.get(https)
            alive.append(https + '\n')
    

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


    probe()
    screenshot(timestamp)
    return
