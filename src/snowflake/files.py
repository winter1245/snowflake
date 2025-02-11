from selenium import webdriver

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

def screenshot(page):
    
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(page)
    driver.save_screenshot('screenshot.png')
    driver.quit()
    
    return


def cycle():
    screenshot('https://example.com')
    return
