from time import time 
from selenium import webdriver

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
        folder =subdomain.replace('.','_')[-1]

        try:
            driver.get(http)

            source = driver.page_source
            sourcelist = source.split('\n')

            helper.writeFile(f'data/{folder}/{timestamp}/httpsource.html',sourcelist)
            driver.save_screenshot(f'data/{folder}/{timestamp}/httpscreenshot.png')

        except selenium.common.exceptions.WebDriverException:
            print(http + 'not found')    

        try:
            driver.get(https)

            source = driver.page_source
            sourcelist = source.split('\n')

            helper.writeFile(f'data/{folder}/{timestamp}/source.html',sourcelist)
            driver.save_screenshot(f'data/{folder}/{timestamp}/screenshot.png')

        except selenium.common.exceptions.WebDriverException:
            print(https + 'not found')    



    driver.quit()
        
    return


def cycle():


    screenshot()
    return
