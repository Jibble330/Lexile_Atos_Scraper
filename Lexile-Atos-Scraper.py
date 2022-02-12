#Selenium requires lots of imports for certain things
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

path = "chromedriver.exe"
ser = Service(path)

def LexileSearch(ISBN):
    baseurl = "https://hub.lexile.com/find-a-book/book-details/"
    searchurl = baseurl + ISBN #Lexile's urls are built around ISBN's, which makes it considerably easier(and faster)
    options = webdriver.ChromeOptions()
#    options.binary_location = "GoogleChromePortable.exe" #Uncomment if using a portable version of Google Chrome (must be in same directory as the program)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless") #Comment this line if you want to see what's going on
    options.add_argument("--no-sandbox")
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(searchurl)
    classname = "sc-ckRZPU.hOvGlS"
    try:
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
    except TimeoutException:
        driver.quit()
        return [1]
    #Scrape Lexile level
    fnd_CLASSNAME = driver.find_element(By.CLASS_NAME, classname)
    LexileText = fnd_CLASSNAME.text
    driver.quit()
    return [0, LexileText]
        
def ARSearch(ISBN):
    searchurl = "https://www.arbookfind.com/default.aspx"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")#Comment this line if you want to see what's going on
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(searchurl)
    classname = "quick-search-field"
    CssSelector = "#radLibrarian"
    try:  #Wait for page to load
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, CssSelector)))
    except TimeoutException:
        driver.quit()
        return [1]
    #Select librarian on radio type popup
    driver.find_element(By.CSS_SELECTOR, CssSelector).click()
    driver.find_element(By.CSS_SELECTOR, "#btnSubmitUserType").click()
    try:  #Wait for page to load
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
    except TimeoutException:
        driver.quit()
        return [1]
    #Search for ISBN
    text_area = driver.find_element(By.CLASS_NAME, classname)
    text_area.send_keys(ISBN)
    text_area.send_keys(Keys.ENTER)
    TitleSelector = "#book-title"
    try:  #Wait for page to load
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, TitleSelector)))
    except TimeoutException:
        driver.quit()
        return [1]
    #Click on title href
    driver.find_element(By.CSS_SELECTOR, TitleSelector).click()
    AtosSelector = "#ctl00_ContentPlaceHolder1_ucBookDetail_lblBookLevel"
    try:  #Wait for page to load
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, AtosSelector)))
    except TimeoutException:
        driver.quit()
        return [1]
    #Scrape ATOS level
    Atos = driver.find_element(By.CSS_SELECTOR, AtosSelector)
    Atos = Atos.text
    return [0, Atos]
def main():
    ISBN = str(input("Please scan barcode or input ISBN: "))
    Lexile = LexileSearch(ISBN)
    ARInfo = ARSearch(ISBN)
    if Lexile[0] == 0:
        print(f'Lexile: {Lexile[1]}')
    else:
        print("Could not find book by that ISBN in Lexile")
    if ARInfo[0] == 0:
        print(f'AR Level: {ARInfo[1]}')
    else:
        print("Could not find book by that ISBN in AR Book Finder")
    
if __name__ == '__main__':
    main()
