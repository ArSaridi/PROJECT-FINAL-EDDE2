def web_driver():
    import sys

    WEB_DRIVER_PATH = "./"

    sys.path.insert(0, WEB_DRIVER_PATH)

    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome('chromedriver', chrome_options=chrome_options)
