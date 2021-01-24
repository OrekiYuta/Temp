import time
import mariadb
import requests

from randomUA import getUserAgent
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions

phoneNum = 18800126264


def ChromeOpen():
    headers = f"user-agent='{getUserAgent()}'"
    print(headers)
    options = ChromeOptions()
    options.add_argument(headers)
    # options.add_argument("--headless")  # 隐藏浏览器
    options.add_argument("--no-sandbox")  # linux 需要禁用这个
    options.add_argument("--disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片资源
    # chrome = Chrome(executable_path="./chromedriver.exe", options=options) # 路径加载驱动
    chrome = Chrome(options=options)
    return chrome


def ChromeClose(chrome):
    chrome.close()


# 青年创业网
def qncyw(chrome):
    name = "qncyw"
    setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        url = "https://www.qncyw.com/site/signup"
        chrome.get(url)
        chrome.find_element_by_css_selector('#username').send_keys(phoneNum)
        chrome.find_element_by_css_selector('#btnSendCode').click()

    except NoSuchElementException as error:
        print(error)
        chrome.get_screenshot_as_file(f"./error/{name}+{setDateTime}.png")
    finally:
        print(f"{name} already completed at {setDateTime}")


# ChromeOpen()

# acfun
def acfun(chrome):
    name = "acfun"
    setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        url = "https://www.acfun.cn/reg/"
        chrome.get(url)
        chrome.find_element_by_css_selector('#reg > div.reg-container > div > div.reg-form-wrapper > form > div:nth-child(1) > span > input').send_keys(phoneNum)
        chrome.find_element_by_css_selector('#reg > div.reg-container > div > div.reg-form-wrapper > form > div:nth-child(4) > span > div.ac-input-suffix-item > span').click()

    except NoSuchElementException as error:
        print(error)
        chrome.get_screenshot_as_file(f"./error/{name}+{setDateTime}.png")
    finally:
        print(f"{name} already completed at {setDateTime}")


chrome_open = ChromeOpen()
acfun(chrome_open)


def boom():
    return
