from selenium import webdriver

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

def screenshot(page):
    
    browser = webdriver.Firefox()
    browser.get(page)
    browser.save_screenshot('screenshot.png')
    return


def cycle():
    screenshot('example.com')
    return
