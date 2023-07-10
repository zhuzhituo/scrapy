import scrapy
import pymysql as pmq
import time
import json
import configparser
from pymysql.converters import escape_string

class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Referer': 'https://www.toutiao.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'Cookie': 'msToken=tZ-rDoGHbMsEQlALGlkT-DvUFK--miZuJEslWKZkbrrEEGcGMOZamJnssGwompFcTn0qki2rCF6kr-FW9tbEh9d3aGCyOxCn1B3x6gqpqe4=; __ac_signature=_02B4Z6wo00f01Dq8tlQAAIDBsfcttUrTkQw6nLLAAGoSa2; tt_webid=7252173497236784697; ttcid=4c339ffca7d0466a9d8bc54cf03ff21360; local_city_cache=%E5%8E%A6%E9%97%A8; csrftoken=88127be78bc55e971f0b4aecd701d61d; _ga=GA1.1.461851041.1688528233; s_v_web_id=verify_ljp643g1_Fl40nE0S_u9ZV_4ZC1_9Rca_UID88oLMR67m; _ga_QEHZPBE5HH=GS1.1.1688717547.2.0.1688717547.0.0.0; tt_scid=OoTRzNw1g2MlP-ZREPj9ZtElRv5jtY2SvLdXMP9QzSV-TqDykF25hxYxPcbkqnomac96; ttwid=1%7CUNOPuoBN8sufFFAmeCyWum1xcFO1FvGMUZEzujWm78s%7C1688717546%7Cea5648ba2e8a96009daa8cfc26e4d17bcfe39d4744641329781de61bea93d04e',
        }

        url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc&_signature=_02B4Z6wo001015WuBHAAAIDCHuWfk-kci0-VigDAAIHXpI5GZClJqUUtGu7jid7n7U2Lq9rf3TkesRiom.K0.jzjkBGT7WfGj8elrD28oG5U-eb0y4To48XsUI73QKA2nBmK8SmVMNcx0OYkf9'
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        self.insert_data(str(response.body.decode('utf-8')))
        # 处理响应数据

    def insert_data(self, data):
        config = configparser.ConfigParser()
        config.read('config.ini')
        con = pmq.connect(host = config['mysql']['host'], user=config['mysql']['user'], password=config['mysql']['pwd'], db=config['mysql']['db'])
        # 操作游标
        cur = con.cursor()
        data = data.strip('b')
        data = data.strip('"')
        data = data.strip("'")

        result = {}

        data = json.loads(data)

        if 'fixed_top_data' in data and data['fixed_top_data']:
            result['hot_top'] = {}
            result['hot_top']['word'] = data['data']['fixed_top_data'][0]['Title']
            result['hot_top']['url'] = data['data']['fixed_top_data'][0]['icon_desc_color']

        i = 0

        if 'data' in data and data['data']:
            result['list'] = []
            for arr in data['data']:
                result['list'].append(i)
                temp = {}
                temp['small_icon_desc'] = arr['Label']
                temp['word'] = arr['Title']
                temp['hot_value'] = arr['HotValue']
                temp['realpos'] = i + 1
                temp['url'] = arr['Url']
                result['list'][i] = temp
                i = i + 1

        json_data = json.dumps(result)

        sql = "INSERT INTO xmnnyq_outernet_data(content,type,create_time) VALUES('" + escape_string(json_data) + "',3," + str(int(time.time())) + ")"

        cur.execute(sql)
        # 提交到数据库执行
        con.commit()
        pass
