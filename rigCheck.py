import time
import natsort
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def getRigs():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://pool.binance.com/en/earnings?urlParams=Qz3MVUD4DjzR0wrKEcNmgmAYaWoz8WcuNqQvK0uxk1E08823")
    time.sleep(1)
    driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
    elem = driver.find_elements(by=By.CLASS_NAME, value="item")
    time.sleep(1)
    elem[2].click()
    time.sleep(1)
    devices =  driver.find_elements(by=By.CLASS_NAME, value="second")
    hashrates = driver.find_elements(by=By.CLASS_NAME, value="third")
    devices.pop(0)
    hashrates.pop(0)
    devices.pop()
    hashrates.pop()
    rigs = {}
    for i,j in zip(devices,hashrates):
        rigs[i.text] = j.text;
    driver.close()
    sortedRigs = natsort.natsorted(rigs.items())
    return dict(sortedRigs)