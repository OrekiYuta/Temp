import os
import time
import mariadb
import requests
import yaml
from randomUA import getUserAgent
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

phoneNum = 18800126264
# phoneNum = 18800126263


def ChromeOpen():
    # headers = f"user-agent='{getUserAgent()}'"
    headers = 'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36" '
    print(headers)
    options = ChromeOptions()
    options.add_argument(headers)
    # options.add_argument("--headless")  # 隐藏浏览器
    options.add_argument("--no-sandbox")  # linux 需要禁用这个
    options.add_argument("–incognito")
    options.add_argument("--disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片资源
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', prefs)  # 禁止弹窗
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
'''
# 获取当前文件路径 F:/Code/Temp/PythonDemo/Pure/eboo
print(os.path.dirname(__file__))
# 获取当前文件 realpath  ('F:\\Code\\Temp\\PythonDemo\\Pure\\eboo', 'eboo.py')
print(os.path.split(os.path.realpath(__file__)))
# F:\Code\Temp\PythonDemo\Pure\eboo
filepath = os.path.split(os.path.realpath(__file__))[0]
print(filepath)
# 获取与 filepath 同级目录下的文件
path_join = os.path.join(filepath, 'properties.yaml')
print(path_join)

filename = os.path.join(os.path.dirname(__file__), 'properties.yaml'.replace("\\", "/"))
t = open(filename, encoding='utf-8')
print(yaml.load(t, Loader=yaml.FullLoader))
'''

file_path = os.path.join(os.path.dirname(__file__), 'properties.yaml'.replace("\\", "/"))
yaml_load = yaml.load(open(file_path, encoding='utf-8'), Loader=yaml.FullLoader)
# print(yaml_load)
# print(type(yaml_load))
'''
for prop in yaml_load:
    # print(prop['title'])
    print(type(prop))
    # for site in prop:
    #     print(site)
'''


# for site in yaml_load['Sites']:
#     print(site['url'])


def getProperties():
    file_path = os.path.join(os.path.dirname(__file__), 'properties.yaml'.replace("\\", "/"))
    yaml_load = yaml.load(open(file_path, encoding='utf-8'), Loader=yaml.FullLoader)
    return yaml_load


# def __call__(self, driver):
#     try:
#         alert = driver.switch_to.alert
#         alert.text
#         return alert
#     except NoAlertPresentException:
#         return False


def ebooyaml(chrome):
    for item in yaml_load['Sites']:
        # 判断几个参数同时不为空
        if all([item['url'], item['name'], item['phoneInputParser'], item['sendButtonParser']]):
            itemUrl = item['url']
            itemName = item['name']
            itemParser = 'xpath'
            setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            # chrome.switch_to.alert().dismiss()
            chrome.get(itemUrl)
            chrome.refresh()  # 刷新一下，有的站点在启动浏览器的时候检测了是否开启自动化工具

            time.sleep(1)

            if item['parser'] == 'selector':
                itemParser = 'find_element_by_css_selector'
            elif item['parser'] == 'xpath':
                itemParser = 'find_element_by_xpath'
            else:
                print(f"parser: '{item['parser']}' is Invalid Parameter")
                continue

            # print("-----------------------------------------------------------")
            print(f"{setDateTime} -- {itemName} start ")
            # chrome 对象通过 __getattribute__ 方法去执行名为 itemParser 变量值的函数

            try:
                chrome.__getattribute__(itemParser)(item['phoneInputParser']).send_keys(phoneNum)
                # 有的页面在输入后需要移出光标做校验完毕才显示验证码按钮
                # ActionChains(chrome).move_by_offset(10, 200).perform()  # 左键点击
                ActionChains(chrome).move_by_offset(0, 0).context_click().perform()  # 右键
                time.sleep(1)
                chrome.__getattribute__(itemParser)(item['sendButtonParser']).click()

            except Exception as error:
                print(f"{itemName} ---> {error}")
                print(f"{setDateTime} -- {itemName} expectation failed")
                # chrome.get_screenshot_as_file('./error/' + itemName + '_' + setDateTime + '.png')
                continue

            # 判断是否存在弹窗提示
            chromeAlert = expected_conditions.alert_is_present()(chrome)
            if chromeAlert:
                print(chromeAlert.text)
                # print(chrome.switch_to.alert.text)
                chrome.switch_to.alert.dismiss()

            print(f"{setDateTime} -- {itemName} completed")
            print("-----------------------------------------------------------")

            # finally:
            #     print(f"{itemName} already completed at {setDateTime}")
            #     print("-----------------------------------------------------------")
        else:
            print("Params[url,name,phoneInputParser,sendButtonParser] Can't be Null")


chrome_open = ChromeOpen()
ebooyaml(chrome_open)
# ChromeClose(chrome_open)

# def eboo(chrome):
#     for item in config:
#         itemName = item['name']
#         itemUrl = item['url']
#         itemParser = ''
#         setDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#
#         try:
#             chrome.get(itemUrl)
#
#             if item['parser'] == 'selector':
#                 itemParser = 'find_element_by_css_selector'
#             elif item['parser'] == 'xpath':
#                 itemParser = 'find_element_by_xpath'
#
#             # chrome 对象通过 __getattribute__ 方法去执行名为 itemParser 变量值的函数
#             chrome.__getattribute__(itemParser)(item['phoneInputParser']).send_keys(phoneNum)
#             chrome.__getattribute__(itemParser)(item['sendButtonParser']).click()
#
#         except NoSuchElementException as error:
#             print(f"{itemName} ---> {error}")
#             chrome.get_screenshot_as_file('./error/' + itemName + '_' + setDateTime + '.png')
#         finally:
#             print(f"{itemName} already completed at {setDateTime}")


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
