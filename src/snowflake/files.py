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
        
        print('debug')
        http= 'http://' + subdomain
        https = 'https://' + subdomain

        try:
            r = requests.get(http)
            alive.append(http)
    

        except requests.exceptions.RequestException:  
            pass

        try:
            r = requests.get(https)
            alive.append(https)
    

        except requests.exceptions.RequestException:  
            pass
         
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} probe subdomain [{fl.index(subdomain)+1} of {len(fl)}]')     
            sys.stdout.flush()
        sleep(2)

    helper.appendFile('alive.txt',alive)
    return


def screenshot(timestamp):
    
    fl = helper.fromFile('alive.txt')
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    
    for subdomain in fl:
        
        http = 'http://' + subdomain
        https = 'https://' + subdomain
        folder =subdomain.replace('.','_')[:-1]
        path = f'data/{folder}/{timestamp}/'
        if not os.path.isdir(path):
            os.makedirs(path)
        try:
            driver.get(http)

            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            
            try:
                with open(f'{path}httpsource.html', 'w') as file:
                    file.write(soup.prettify())

            except OSError:
                print(f"Writing to {path} failed")
            
            driver.save_screenshot(f'{path}httpscreenshot.png')

        except selenium.common.exceptions.WebDriverException:
            print(http + 'not found')    

        try:
            driver.get(https)

            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            try:
                with open(f'{path}source.html', 'w') as file:
                    file.write(soup.prettify())

            except OSError:
                print(f"Writing to {path} failed")
            
            driver.save_screenshot(f'{path}screenshot.png')

        except selenium.common.exceptions.WebDriverException:
            print(https + 'not found')    
        
        sleep(5)
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} screenshot website [{fl.index(subdomain)+1} of {len(fl)}]')     
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
