from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getHTML(webpage):
    """Uses selenium to get HTML of a webpage"""

    # configure webdriver
    options = Options()
    options.headless = True  # hide GUI


    # configure chrome browser to not load images and javascript
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option(
    #     # this will disable image loading
    #     "prefs", {"profile.managed_default_content_settings.images": 2}
    # )

    driver = webdriver.Chrome(options=options)

    driver.get(webpage)
    element = WebDriverWait(driver=driver, timeout=5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'article')) #Mer effektivt å finne noe annet? Denne funker ikke for alle nettsider
)
    HTML = driver.page_source

    driver.quit()
    return HTML