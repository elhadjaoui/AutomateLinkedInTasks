import subprocess
import sys

try :
    from dotenv import dotenv_values, load_dotenv
except ModuleNotFoundError:
        print("module 'dotenv' is not installed")
        print("installing 'python-dotenv'..")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])
try :
    from selenium import webdriver
except ModuleNotFoundError:
        print("module 'selenium' is not installed")
        print("installing 'selenium'..")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

try :
    from webdriver_manager.chrome import ChromeDriverManager
except ModuleNotFoundError:
        print("module 'webdriver_manager' is not installed")
        print("installing 'webdriver_manager'..")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'webdriver_manager'])
import time

from selenium.webdriver.support import expected_conditions as EC

RED='\033[0;31m'   #ANSI ESCAPE CODE
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

print(CYAN, "Launching script...")
options = Options()
options.add_argument('--lang=en-US')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
config = dotenv_values("data.env")
driver.maximize_window()

#div[role="listbox"]>div>div

def login(username1, password1):

    driver.get("https://linkedin.com/")
    try:
        username = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(EC.presence_of_element_located((By.NAME, 'session_key')))
        password = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(EC.presence_of_element_located((By.NAME, 'session_password')))

        username.click()
        username.clear()
        username.send_keys(username1)

        password.click()
        password.clear()
        password.send_keys(password1)

        login = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        login.click()
    except Exception as err:
        print(err)
def check_word(string):
        if not config[string] :
                return 1
        return 0
def filter_by_location(loc):
    try :
        location = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Locations"]')))
        location.click()
        time.sleep(float(config["TIMETOWAIT"]))
        input_location = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Add a location"]')))
        input_location.click()
        input_location.clear()
        input_location.send_keys(loc)
        time.sleep(float(config["TIMETOWAIT"]))
        exact_location = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="listbox"]>div>div')))
        exact_location.click()
        time.sleep(float(config["TIMETOWAIT"]))
        show_results = WebDriverWait(driver, float(config["TIMETOWAIT"])).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ember1959"]')))
        show_results.click()
    except (NoSuchElementException, Exception) as err:
        print(err)
        print("Something went wrong..")
        driver.quit()

def filter_by_skill():
    try:
        keyword = ""
        hash = config["SKILL"].split(',')
        if len(hash) < 1:
            print("Skill shouldn't be empty")      
        else :
            length = len(hash)
            for x in range(length) :
           
                keyword += hash[x]
                if x + 1 >= length :
                    break
                keyword += "%2C"
        driver.get("https://www.linkedin.com/search/results/people/?keywords="+keyword+"&origin=SWITCH_SEARCH_VERTICAL&sid=N8%3B")
        time.sleep(float(config["TIMETOWAIT"]))
        for location in config["LOCATION"].split(','):
            filter_by_location(location)
        time.sleep(float(config["TIMETOWAIT"]))

    except Exception as err:
        print(err)
        print("Search input not found please increase TIMETOWAIT")
        driver.quit()




def start():
    login(config["EMAIL"], config["PASSWORD"])
    time.sleep(float(config["TIMETOWAIT"]))
    filter_by_skill()
    print("Done.")
    driver.quit()


start()