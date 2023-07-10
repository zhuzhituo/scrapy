# -*- coding:gbk -*-
import scrapy
import pymysql as pmq
import time
import json
import configparser
from pymysql.converters import escape_string

class WeiboSpider(scrapy.Spider):
    name = "weibo"

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Referer': 'https://weibo.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'Cookie': 'SINAGLOBAL=7514361040414.872.1688613146408; ULV=1688613146437:1:1:1:7514361040414.872.1688613146408:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5egkLFrgLN.J_kIJFgfNsO5JpX5KMhUgL.FoeceheESo-Ne0e2dJLoIEBLxKBLB.2L1K2LxKMLB.2LBo2LxKML1K2LB.-LxKML1K2L1K-t; XSRF-TOKEN=zrD-wOwAJuLVAdb8QQ5_O4lG; ALF=1691310371; SSOLoginState=1688718372; SCF=AuNmI21m8N6isM7k4BB5NPm7_3ehnZ9Cu72NtnKz-hdEgtPeEUHDD1lNTPXf9eZ7PRJ-m7sDmGPwnqY7BJ-UaNA.; SUB=_2A25Jo7x1DeRhGeVI61ET9ivLyD-IHXVq2Kq9rDV8PUNbmtANLWbAkW9NTAO5Co5icizVI1mC3PygyKR8jFYsStbo; WBPSESS=XMMIwdETR_JT96BLYlgiKUcPZc0UK26_4Ai1R20Y3-jxhlLyJMDcxG7spdowx6KuLE5CvZFjV3Xnt5Colk6DBMhHvADCUS8yqUMdHGt81lGY8uXJfA2mkuyOoYwdMINJ71vS9ccvGQzrH6W_ts8fXg==',
        }

        url = 'https://weibo.com/ajax/side/hotSearch'
     #   url = 'http://www.dearlovertech.com/Best-Sellers-rc9096.html?json=1'

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
        # data = data.encode().decode('unicode_escape')
        data = data.strip('b')
        data = data.strip('"')
        data = data.strip("'")

        result = {}

        data = json.loads(data)

        if 'data' in data and 'hotgov' in data['data'] and data['data']['hotgov']:
            result['hot_top'] = {}
            result['hot_top']['note'] = data['data']['hotgov']['note']
            result['hot_top']['word'] = data['data']['hotgov']['word']
            result['hot_top']['icon_desc_color'] = data['data']['hotgov']['icon_desc_color']
            result['hot_top']['small_icon_desc'] = data['data']['hotgov']['small_icon_desc']
            result['hot_top']['name'] = data['data']['hotgov']['name']
            result['hot_top']['url'] = data['data']['hotgov']['url']
            result['hot_top']['is_hot'] = data['data']['hotgov']['is_hot']

        i = 0
        if 'data' in data and 'realtime' in data['data'] and data['data']['realtime']:
            result['list'] = []
            for arr in data['data']['realtime']:
                result['list'].append(i)
                temp = {}
                category = ''
                if 'category' in arr:
                    category = arr['category']
                temp['category'] = category
                small_icon_desc = ''
                if 'small_icon_desc' in arr:
                    small_icon_desc = arr['small_icon_desc']
                temp['small_icon_desc'] = small_icon_desc
                temp['word'] = arr['word']
                temp['hot_value'] = arr['num']
                is_hot = 0
                if 'is_hot' in arr:
                    is_hot = arr['is_hot']
                temp['is_hot'] = is_hot
                temp['note'] = arr['note']
                small_icon_desc_color = ''
                if 'small_icon_desc_color' in arr:
                    small_icon_desc_color = arr['small_icon_desc_color']
                temp['small_icon_desc_color'] = small_icon_desc_color
                real_pos = 0
                if 'realpos' in arr:
                    real_pos = arr['realpos']
                temp['realpos'] = real_pos
                temp['url'] = 'https://s.weibo.com/weibo?q=' + arr['word']
                result['list'][i] = temp
                i = i + 1

        json_data = json.dumps(result)

        sql = "INSERT INTO xmnnyq_outernet_data(content,type,create_time) VALUES('" + escape_string(json_data) + "',1," + str(int(time.time())) + ")"

        cur.execute(sql)
        # 提交到数据库执行
        con.commit()
        pass
