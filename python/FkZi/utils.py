import sys
import time
import mariadb


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def mariadb_conn():
    try:
        conn = mariadb.connect(
            user="root",
            password="raspberry",
            host="192.168.137.47",
            port=3306,
            database="virus"
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


def query(sql, *args):
    """
    :param sql:
    :param args
    :return 返回查询结果 ((),())
    """
    conn, cursor = mariadb_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    mariadb_conn_close(conn, cursor)

    return res


def get_daily_data():
    sql = "select today_confirm,total_nowConfirm," \
          "total_confirm,total_dead,total_deadRate," \
          "total_heal,total_healRate from daily_data " \
          "where setDataTime=(select setDataTime from daily_data " \
          "order by setDataTime desc limit 1)"
    res = query(sql)
    return res[0]


# 地图整体数据
def get_area_data():
    sql = "select province_name_,sum(city_total_confirm_) " \
          "from tencent_virus_data where lastUpdateTime=(" \
          "select lastUpdateTime from tencent_virus_data " \
          "order by lastUpdateTime desc limit 1) " \
          "group by province_name_"
    res = query(sql)
    return res


# 总趋势最近十天
def get_GeneralTrend_data():
    sql = "select today_confirm,total_nowConfirm,total_confirm," \
          "total_dead,total_heal,setDataTime from daily_data " \
          "order by  id desc limit 10"
    res = query(sql)
    return res
# get_GeneralTrend_data()[1:] # 从第二条数据开始取

# 今日有新增确诊的省市
def get_todayNewConfrim_data():
    sql = "select CONCAT(province_name_,'-',city_name_) as province_city," \
          "city_today_confirm_,lastUpdateTime from tencent_virus_data " \
          "where city_today_confirm_ >0 and lastUpdateTime=(" \
          "select lastUpdateTime from tencent_virus_data " \
          "ORDER BY lastUpdateTime desc limit 1 )"

    res = query(sql)
    return res

# 目前各省市累计确诊数
def get_confrimUntilNow():
    sql = "select province_name_,sum(city_total_confirm_),lastUpdateTime " \
          "from tencent_virus_data where lastUpdateTime = ( " \
          "select lastUpdateTime from tencent_virus_data " \
          "order by lastUpdateTime desc limit 1) " \
          "group by province_name_"

    res = query(sql)
    return res

# 获取最新50条热搜数据
def get_hotPoint():
    sql = "select content,setDataTime from  hotpoint ORDER BY id desc LIMIT 50"
    res = query(sql)
    return res



# if __name__ == '__main__':
    # print(get_confrimUntilNow())
