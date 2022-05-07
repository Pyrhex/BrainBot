import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def getDateAndEarnings():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://pool.binance.com/en/earnings?urlParams=Qz3MVUD4DjzR0wrKEcNmgmAYaWoz8WcuNqQvK0uxk1E08823")
    elem = driver.find_elements(by=By.CLASS_NAME, value="item")
    time.sleep(1)
    driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
    time.sleep(1)
    elem[3].click()
    time.sleep(1)
    date = driver.find_elements(by=By.CLASS_NAME, value="col-1")
    earnings = driver.find_elements(by=By.CLASS_NAME, value="col-4")
    todayDate = (date[2].text)
    todayEarnings = (earnings[2].text)
    driver.close()
    return todayDate, todayEarnings

def writeToExcel(date, earnings):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("crypto-organizer-86bcdfe49a98.json", scopes) #access the json key you downloaded earlier 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Crypto Payout") #open sheet
    sheet = sheet.worksheet("Earnings") #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
    firstCol = len(sheet.col_values(1))
    firstRow = len(sheet.row_values(1))
    projCol = firstCol+1
    projRow = firstRow+1
    sheet.update_cell(projCol, 1, "=WEEKNUM(B" + str(projCol) + ", 15)")
    sheet.update_cell(projCol, 2, "/".join(date.split(".")))
    sheet.update_cell(projCol, 3, earnings.split()[0])

info = getDateAndEarnings()
writeToExcel(info[0], info[1])
