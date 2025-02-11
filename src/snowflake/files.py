import sys
from time import time,sleep 
from selenium import webdriver
from bs4 import BeautifulSoup
import os

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

def screenshot():
    
    fl = helper.fromFile('resolved.txt')
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    
    for subdomain in fl:
        
        http = 'http://' + subdomain
        https = 'https://' + subdomain
        timestamp = int(round(time()))
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
        
        sleep(2)
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} screenshot website [{fl.index(subdomain)+1} of {len(fl)}]')     
            sys.stdout.flush()
    
    driver.quit()
    print()
        
    return


def cycle():


    screenshot()
    return
