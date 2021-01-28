import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

res2 = requests.get('http://tianqi.moji.com/', headers=headers)

soup = BeautifulSoup(res2.text, "html.parser")
temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
sd_num = re.search(r'\d+', sd).group()
sd = sd.replace(sd_num, sd_num)
wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
aqi_num = re.search(r'\d+', aqi).group()
aqi = aqi.replace(aqi_num, aqi_num)
info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
sd = sd.replace(' ', '百分之').replace('%', '')
aqi = 'aqi' + aqi

today = datetime.now().date().strftime('%Y year %m month %d day')
text = '早上好！今天是%s,天气%s,温度%s摄氏度,%s,%s,%s,%s' % \
       (today, weather, temp, sd, wind, aqi, info)
print(text)