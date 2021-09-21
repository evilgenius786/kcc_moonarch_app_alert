import json
import time
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram.ext import Updater

t = 1
timeout = 10

debug = False

headless = False
images = False
max = False

incognito = True

coins = ["", "<Loading...>"]
chat_id = -1001580531015
tkn = "Token"


def main():
    driver = getChromeDriver()
    updater = Updater(tkn, use_context=True)
    driver.get("https://kcc.moonarch.app/")
    while True:
        try:
            tbody = driver.find_elements_by_xpath('//tbody')[1]
            if "0 found recently" in driver.page_source:
                print('0 found recently')
            else:
                coin = getElement(tbody, '//td[@aria-colindex="3" and @class="tokenName"]').text.strip()
                if coin not in coins:
                    kcc = (tbody.find_element_by_xpath('./tr[1]/td[4]/div/a[1]').get_attribute(
                        'href').strip())
                    chart = (tbody.find_element_by_xpath('./tr[1]/td[4]/div/a[2]').get_attribute(
                        'href').strip())
                    koffeeswap = (
                        tbody.find_element_by_xpath('./tr[1]/td[4]/div/a[3]').get_attribute(
                            'href').strip())
                    data = {'name': coin, "kcc": kcc, "chart": chart, "koffeeswap": koffeeswap}
                    print(datetime.now(), "*New coin*", coin)
                    print(json.dumps(data, indent=4))
                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['kcc']}">KCC</a>
<a href="{data['koffeeswap']}">Koffeeswap</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
                    coins.append(coin)
                else:
                    print(datetime.now(), coin)
                time.sleep(1)
        except:
            traceback.print_exc()


def click(driver, xpath, js=False):
    if js:
        driver.execute_script("arguments[0].click();", getElement(driver, xpath))
    else:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def getElement(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def sendkeys(driver, xpath, keys, js=False):
    if js:
        driver.execute_script(f"arguments[0].value='{keys}';", getElement(driver, xpath))
    else:
        getElement(driver, xpath).send_keys(keys)


def getChromeDriver(proxy=None):
    options = webdriver.ChromeOptions()
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
    else:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    if max:
        # print("Maximizing Chrome ")
        options.add_argument("--start-maximized")
    if proxy:
        # print(f"Adding proxy: {proxy}")
        options.add_argument(f"--proxy-server={proxy}")
    if incognito:
        # print("Going incognito")
        options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    if not images:
        # print("Turning off images to save bandwidth")
        options.set_preference("permissions.default.image", 2)
    if incognito:
        # print("Enabling incognito mode")
        options.set_preference("browser.privatebrowsing.autostart", True)
    if headless:
        # print("Hiding Firefox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Firefox(options)


if __name__ == "__main__":
    main()
