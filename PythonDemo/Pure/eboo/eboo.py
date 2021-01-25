import time
import mariadb
import requests

from randomUA import getUserAgent
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions

phoneNum = 18800126264


def ChromeOpen():
    # headers = f"user-agent='{getUserAgent()}'"
    headers = 'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0" '
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


config = [{'name': 'qncyw', 'nameCn': '青年创业网', 'url': 'https://www.qncyw.com/site/signup',
           'parser': 'selector',
           'phoneInputParser': '#username',
           'sendButtonParser': '#btnSendCode'},
          {'name': '360doc', 'nameCn': '个人图书馆', 'url': 'http://www.360doc.com/register.aspx',
           'parser': 'selector',
           'phoneInputParser': '#signMobileName',
           'sendButtonParser': '#sign_sendcode'},
          {'name': 'iwgame', 'nameCn': '河岸网络', 'url': 'http://passport.iwgame.com/reg/account/regpage.do',
           'parser': 'xpath',
           'phoneInputParser': '//*[@name="identityId"]',
           'sendButtonParser': '//*[@id="regPersonalForm"]/ul/li[5]/div[1]/em/a'},
          ]


def eboo(chrome):
    for item in config:
        itemName = item['name']
        itemUrl = item['url']
        itemParser = ''
        setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        try:
            chrome.get(itemUrl)

            if item['parser'] == 'selector':
                itemParser = 'find_element_by_css_selector'
            elif item['parser'] == 'xpath':
                itemParser = 'find_element_by_xpath'

            # chrome 对象通过 __getattribute__ 方法去执行名为 itemParser 变量值的函数
            chrome.__getattribute__(itemParser)(item['phoneInputParser']).send_keys(phoneNum)
            chrome.__getattribute__(itemParser)(item['sendButtonParser']).click()

        except NoSuchElementException as error:
            print(f"{itemName} ---> {error}")
            chrome.get_screenshot_as_file('./error/' + itemName + '_' + setDateTime + '.png')
        finally:
            print(f"{itemName} already completed at {setDateTime}")


chrome_open = ChromeOpen()
eboo(chrome_open)


'''
# 青年创业网
def qncyw(chrome):
    name = config[0]['name']
    setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        # url = "https://www.qncyw.com/site/signup"
        url = config[0]['url']
        chrome.get(url)
        # chrome.find_element_by_css_selector('#username').send_keys(phoneNum)
        chrome.find_element_by_css_selector(config[0]['phoneInputParser']).send_keys(phoneNum)
        # chrome.find_element_by_css_selector('#btnSendCode').click()
        chrome.find_element_by_css_selector(config[0]['sendButtonParser']).click()

    except NoSuchElementException as error:
        print(error)
        chrome.get_screenshot_as_file(f"./error/{name}+{setDateTime}.png")
    finally:
        print(f"{name} already completed at {setDateTime}")

# 个人图书馆
def doc(chrome):
    name = "360doc"
    setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        url = "http://www.360doc.com/register.aspx"
        chrome.get(url)
        chrome.find_element_by_css_selector('#signMobileName').send_keys(phoneNum)
        chrome.find_element_by_css_selector('#sign_sendcode').click()

    except NoSuchElementException as error:
        print(error)
        chrome.get_screenshot_as_file(f"./error/{name}+{setDateTime}.png")
    finally:
        print(f"{name} already completed at {setDateTime}")

# 河岸网络
def iwgame(chrome):
    name = "iwgame"
    setDateTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    try:
        url = "http://passport.iwgame.com/reg/account/regpage.do"
        chrome.get(url)

        chrome.find_element_by_xpath('//*[@name="identityId"]').send_keys(phoneNum)
        chrome.find_element_by_xpath('//*[@id="regPersonalForm"]/ul/li[5]/div[1]/em/a').click()

    except NoSuchElementException as error:
        print(f"{name} ---> {error}")
        chrome.get_screenshot_as_file('./error/' + name + '_' + setDateTime + '.png')
    finally:
        print(f"{name} already completed at {setDateTime}")
'''
