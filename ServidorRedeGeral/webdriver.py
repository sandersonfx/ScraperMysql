from selenium import webdriver
        

class Webdriver:
    def __init__(self, download_directory) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('window-size=1024x768')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_directory,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
        
        GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        chrome_options.binary_location = GOOGLE_CHROME_BIN


        self.driver = webdriver.Chrome(options=chrome_options)
        
    def getDriver(self):
        return self.driver