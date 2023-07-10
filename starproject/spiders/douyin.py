# -*- coding:gbk -*-
import scrapy
import pymysql as pmq
import time
import json
import configparser
from pymysql.converters import escape_string

class DouyinSpider(scrapy.Spider):
    name = "douyin"

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Referer': 'https://www.douyin.com/discover',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'Cookie': 'ttwid=1%7CWkN_zhdih2QfkFS6dWaJGv95glmwBO0hyqiffa0oDDo%7C1688527672%7Cafe6852bb391ccf34813fe926df889a93b8ea238352dcbcfa08d1fa69b7a2486; passport_csrf_token=b336bb202ebeb507a52ca319c2c71eb9; passport_csrf_token_default=b336bb202ebeb507a52ca319c2c71eb9; s_v_web_id=verify_ljp5s357_gjTd4XrN_hJQ1_4rAc_AODg_SIoY4wXEp74O; __bd_ticket_guard_local_probe=1688527673341; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEekNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRXVsZTl4czNNcTQzcGdpZVJyVHJlOFJkeVxyXG5zTm1OeExFMzE4U2NRWXVTaUkxbm9ZSWMrMGtnajRLRWZNWGlsNUR1QlQ3NmRpRVN2Y2xEQi9PUEVmMTBuNkFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU1FBd1JnSWhBTGwxWUJUb28zcDlsV3prS3gwbUlaRDFSWHBsWGZvY0JkZ1lPbmkrckJicFxyXG5BaUVBMlZFbjJuaXd4KytnUFp5V3VVbmpPYm9GVzVmNUJzUHlVV0duU2pxYkxjTT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; ttcid=e5e6f5fea2a040bb886c3c29097cee9429; SEARCH_RESULT_LIST_TYPE=%22single%22; douyin.com; device_web_cpu_core=12; device_web_memory_size=8; webcast_local_quality=null; strategyABtestKey=%221688700765.752%22; csrf_session_id=5c5c5ad604e2a49a954b35f419bb74b6; xgplayer_user_id=50736998750; download_guide=%223%2F20230707%2F0%22; pwa2=%220%7C0%7C3%7C0%22; __ac_nonce=064a7ad9e00b1453c57cc; __ac_signature=_02B4Z6wo00f01KRPftwAAIDBLwTlPUvoObSkb3pAAE25jTXkRIXeUzzHch0SI5CJafk-ImnXY3j9Ew6ypJt48qVgjwExMMcjmODMm3c5H1aOqOFCho.z2ux67xVK67ORDcBw5HqhTI46khSZc5; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1689315662019%2C%22type%22%3Anull%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; home_can_add_dy_2_desktop=%221%22; msToken=Qwldfa7k4j_fhNXMWDoGJMnQ1cTP44xciuqjR_28JZ46ZN8-H263nrkA7SEdGNxYn5yqen8YDs8veQO4_ZyIKgt1-rFynHNmcicp9RKoIsyJS7N_6m3q; msToken=DTOjc_iZzPGKFZq9wvDPflHQzw_FID3A91CNJt-7hhmHVABaft5HUgl5QbKUqkFxgh1EKr6Yi71gp0XniBdwbnLbTJhkagwKThWrKvSOcj5ZnmBG1QJn613O_b-E2A==; tt_scid=OueK7RonCwnFeZtk1WX1jzr6s8GLWKXdJXzIArXotkbBkuOXxzTr-m4pfKWO6.34394a',
        }

        url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=0&board_sub_type=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1680&screen_height=1050&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=101.0.4951.64&browser_online=true&engine_name=Blink&engine_version=101.0.4951.64&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7252171049223407107&msToken=uSBmWSwRCvBmynztZSyNF8N3bFN7XOU0c6oR3qC4q4lpfVM6B2Rj-AQzIE0tbFkdBoKXg5SeT21jvb3rOIA92kTA7iPVir4sLwiCc1-QM1aJJrObtSDHKWI1DP6s0g==&X-Bogus=DFSzswVuRtXANnVttJDEB-t/pL3e'
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
        i = 0
        # lable 1 新  5  首发   3  热   8 独家
        if 'data' in data and 'word_list' in data['data'] and data['data']['word_list']:
            result['list'] = []
            result['hot_top'] = {}
            for arr in data['data']['word_list']:
                if i == 0 :
                    result['hot_top']['label'] = arr['label']
                    result['hot_top']['word'] = arr['word']
                    label = ''
                    if arr['label'] == 1 :
                        label = '新'
                    elif arr['label'] == 3 :
                        label = '热'
                    elif arr['label'] == 5:
                        label = '首发'
                    elif arr['label'] == 8:
                        label = '独家'
                    result['hot_top']['small_icon_desc'] = label
                    result['hot_top']['url'] = 'https://www.douyin.com/hot/' + arr['sentence_id']
                else :
                    result['list'].append(i)
                    temp = {}
                    temp['small_icon_desc'] = arr['label']
                    temp['word'] = arr['word']
                    temp['hot_value'] = arr['hot_value']
                    temp['view_count'] = arr['view_count']
                    temp['label'] = arr['label']
                    temp['realpos'] = arr['position']
                    temp['url'] = 'https://www.douyin.com/hot/' + arr['sentence_id']
                    result['list'][i - 1] = temp
                i = i + 1

        json_data = json.dumps(result)

        sql = "INSERT INTO xmnnyq_outernet_data(content,type,create_time) VALUES('" + escape_string(json_data) + "',2," + str(int(time.time())) + ")"

        cur.execute(sql)
        # 提交到数据库执行
        con.commit()
        pass
