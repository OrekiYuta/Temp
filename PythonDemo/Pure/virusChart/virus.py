import sys
import time
import json
import mariadb
import requests
import traceback
from datetime import datetime
from selenium.webdriver import Chrome, ChromeOptions

# https://www.qq.com/
# https://sa.sogou.com/new-weball/page/sgs/epidemic?type_page=VR
# http://top.baidu.com/buzz?b=1&fr=topindex


# http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml
from bs4 import BeautifulSoup


def get_tencent_virus_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

    # https://news.qq.com/zt2020/page/feiyan.htm#/
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    getSource = json.loads(res.text)
    sourceData = json.loads(getSource["data"])

    lastUpdateTime = sourceData["lastUpdateTime"]  # 最后更新时间
    chinaTotal = sourceData["chinaTotal"]  # 总情况
    chinaAdd = sourceData["chinaAdd"]  # 总确诊
    areaTree = sourceData["areaTree"]  # 国家

    # 国家列表,中国
    name = areaTree[0]["name"]  # 中国
    today = areaTree[0]["today"]  # 今天新增确诊
    total = areaTree[0]["total"]  # 今日总情况
    provinces = areaTree[0]["children"]  # 34个省份

    # print(name)
    # print(today)
    # print(total)

    # 今日确诊，目前确诊，总确诊，总死亡数，总死亡概率，总康复数，总康复概率
    daily_data = [name, today["confirm"], total["nowConfirm"], total["confirm"], total["dead"], total["deadRate"],
                  total["heal"], total["healRate"]]

    today_details = []
    for province in provinces:
        # print(province["name"])  # 省名
        # print(province["today"])
        # print(province["total"])
        province_name_ = province["name"]

        # 省所属城市
        for city in province["children"]:
            city_name_ = city["name"]
            city_today_confirm_ = city["today"]["confirm"]  # 该城市今日确诊
            city_total_confirm_ = city["total"]["confirm"]  # 该城市总确诊
            city_total_heal_ = city["total"]["heal"]  # 该城市总康复
            city_total_heal_rate_ = city["total"]["healRate"]  # 该城市总康复概率
            city_total_dead_ = city["total"]["dead"]  # 该城市总死亡
            city_total_dead_rate_ = city["total"]["deadRate"]  # 该城市总死亡概率
            today_details.append([lastUpdateTime, province_name_, city_name_, city_today_confirm_,
                                  city_total_confirm_, city_total_heal_, city_total_heal_rate_,
                                  city_total_dead_, city_total_dead_rate_
                                  ])

    return today_details, daily_data


# def mariadb_conn(dbUser, dbPassword, dbHost, dbPort, dbName):
def mariadb_conn():
    try:
        conn = mariadb.connect(
            user="root",
            password="raspberry",
            host="192.168.137.47",
            port=3306,
            database="virus"
            # user=dbUser,
            # password=dbPassword,
            # host=dbHost,
            # port=dbPort,
            # database=dbName
        )
        cursor = conn.cursor()
        return conn, cursor

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def mariadb_conn_close(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 更新每日的详情数据
def update_virus_data():
    cursor = None
    conn = None
    try:
        virus_data = get_tencent_virus_data()[0]
        # conn, cursor = mariadb_conn("root", "raspberry", "192.168.137.165", 3306, "virus")
        conn, cursor = mariadb_conn()
        setDataTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql_insert_data = "insert into tencent_virus_data(lastUpdateTime,province_name_," \
                          "city_name_,city_today_confirm_,city_total_confirm_," \
                          "city_total_heal_,city_total_heal_rate_," \
                          "city_total_dead_,city_total_dead_rate_," \
                          "setDataTime"") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 取数据库最后一个记录的时间字段
        sql_lastTime = "select lastUpdateTime from tencent_virus_data order by id desc limit 1"
        cursor.execute(sql_lastTime)
        lastUpdateTime = cursor.fetchone()

        # 第一次初始化数据
        if lastUpdateTime is None:
            print(f"{time.asctime()}    --->    滴滴！初始化最初的数据！")
            for item in virus_data:
                item.append(setDataTime)
                print(item)
                cursor.execute(sql_insert_data, item)
            conn.commit()
            print(f"{time.asctime()}    --->    嗒嗒！初始化数据完毕！")

        # 非第一次更新数据
        else:
            # virus_data[0][0] 拿第一条数据的时间字段,因为每条数据时间都是一样的
            dataNowTime = datetime.strptime(virus_data[0][0], '%Y-%m-%d %H:%M:%S')
            # 数据库最新记录时间 与 当前请求的数据时间对比，判断是否更新数据
            if dataNowTime > lastUpdateTime[0]:
                print(f"{time.asctime()}    --->    滴滴！开始更新最新数据！")
                for item in virus_data:
                    item.append(setDataTime)
                    cursor.execute(sql_insert_data, item)
                conn.commit()
                print(f"{time.asctime()}    --->    嗒嗒！更新最新数据完毕！")
            else:
                print(f"{time.asctime()}    --->    嗯！已是最新数据！")

    except:
        traceback.print_exc()
    finally:
        mariadb_conn_close(conn, cursor)


# 更新每日的汇总数据
def update_daily_data():
    cursor = None
    conn = None
    try:
        daily_data = get_tencent_virus_data()[1]
        # conn, cursor = mariadb_conn("root", "raspberry", "192.168.137.165", 3306, "virus")
        conn, cursor = mariadb_conn()
        setDataTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql_insert_data = "insert into daily_data(country,today_confirm," \
                          "total_nowConfirm,total_confirm,total_dead," \
                          "total_deadRate,total_heal," \
                          "total_healRate,setDataTime"") values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 这里因为是一天只更新一次，所以做个日期判断
        sql_lastUpdateTime = "select date_format(setDataTime,'%Y-%m-%d') " \
                             "from daily_data order by id desc limit 1;"

        NowTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        cursor.execute(sql_lastUpdateTime)
        lastUpdateTime = cursor.fetchone()[0]

        if NowTime > lastUpdateTime:
            daily_data.append(setDataTime)
            print(f"{time.asctime()}    --->    哔哔！开始更新每日汇总数据")
            print(daily_data)
            cursor.execute(sql_insert_data, daily_data)
            conn.commit()
            print(f"{time.asctime()}    --->    哔哔！更新每日汇总数据完毕")
        else:
            print(f"{time.asctime()}    --->    哎呀！今日的汇总数据已是最新的了")



    except:
        traceback.print_exc()
    finally:
        mariadb_conn_close(conn, cursor)


"""
# 搜狗热搜 热搜用的JS加载，用 selenium 抓取 / 疫情数据是json可以获取
# selenium
# pip install selenium
# https://npm.taobao.org/mirrors/chromedriver/ 下载符合浏览器的驱动
"""


def sogou_hotSearch():
    headers = 'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; ' \
              'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1" '

    url = "https://sa.sogou.com/new-weball/page/sgs/epidemic?type_page=VR"

    # res = requests.get(url, headers=headers)
    # res.encoding = "utf-8"
    # html = res.text
    # soup = BeautifulSoup(html, "lxml")
    # soup.find_all(name="ul", attrs={"class": "list-fh"})
    # print(soup.text)

    # 把 Chrome()对象放在方法里,方法执行完毕谷歌浏览器对象就会关闭,打开的谷歌浏览器页面也就随着关闭,放在全局变量就可以了

    # chorme =Chrome(r"chromedriver.exe")
    # https://zhuanlan.zhihu.com/p/60852696 ChromeOptions 配置参数
    # options = Options()

    options = ChromeOptions()
    options.add_argument(headers)
    options.add_argument("--headless")  # 隐藏浏览器
    options.add_argument("--no-sandbox")  # linux 需要禁用这个
    options.add_argument("--disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片资源
    # chrome = Chrome(str="./chromedriver.exe", options=options) # 路径加载驱动
    chrome = Chrome(options=options)
    chrome.get(url)
    # ul = chrome.find_element_by_class_name("list-fh")
    el_lis = chrome.find_elements_by_xpath('//*[@id="no_active_pane"]/div/div/div[2]/ul/li')
    # for el_li in el_lis:
    #     print(el_li.text)
    content = [el_li.text for el_li in el_lis]
    chrome.close()

    return content


def baidu_hotPoint():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    url = "http://top.baidu.com/buzz?b=1&fr=topindex"

    res = requests.get(url, headers=headers)
    res.encoding = "gb2312"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    titles = soup.find_all(name="a", attrs={"class": "list-title"})
    content = [title.text for title in titles]

    return content


def tencent_hotPoint():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    url = "https://www.qq.com/"
    res = requests.get(url, headers=headers)
    res.encoding = "gb2312"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    # titles = soup.find_all(name="div", attrs={"id": "tab-news-02"})
    titles = soup.select('#tab-news-02>ul>li>a')
    content = []
    for title in titles:
        content.append(title.text)
    return content


def update_hotPoint():
    cursor = None
    conn = None
    try:
        sogouContent = sogou_hotSearch()
        baiduContent = baidu_hotPoint()
        tenncentContent = tencent_hotPoint()

        ContentList = {"搜狗": sogouContent, "百度": baiduContent, "腾讯": tenncentContent}

        conn, cursor = mariadb_conn()
        setDataTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = "insert into hotpoint(content,setDataTime) values (%s,%s)"

        for k, v in ContentList.items():
            print(k)
            print(v)
            print(f"{time.asctime()}    --->    嘻嘻！开始更新{k}热点数据")
            for content in v:
                print(content)
                cursor.execute(sql, (content, setDataTime))
            conn.commit()
            print(f"{time.asctime()}    --->    哟嚯！更新{k}热点数据完毕")
            print("----------------------------------------------------------------")
    except:
        traceback.print_exc()
    finally:
        mariadb_conn_close(conn, cursor)


# update_hotPoint()
#
# update_daily_data()
#
# update_virus_data()


if __name__ == '__main__':
    length = len(sys.argv)
    if length == 1:
        s = """
                请输入参数：
                dd 更新详细数据
                vd 更新汇总数据
                hp 更新热点信息
            """
        print(s)
    else:
        order = sys.argv[1]
        if order == "vd":
            update_virus_data()
        elif order == "dd":
            update_daily_data()
        elif order == "hp":
            update_hotPoint()
