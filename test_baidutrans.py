'''

测试百度翻译

查询是否有requests
conda search requests

安装
conda install requests

'''

import requests
import random
import json
from hashlib import md5

# Set your own appid/appkey.
appid = '20240212001962846'
appkey = 'VTOmOXWJvflYLCQHAfW8'


class BaiduTrans:
    def __init__(self):
        pass

    # Generate salt and sign
    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def Trans(self, query, from_lang='en', to_lang='zh'):
        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        # from_lang = 'en'
        # to_lang = 'zh'

        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        salt = random.randint(32768, 65536)
        sign = self.make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()

        # Show response
        print(json.dumps(result, indent=4, ensure_ascii=False))

        # 解析json
        print(f"from = {result['from']}")

        trans_result = result['trans_result']

        for item in trans_result:
            print(f"src = {item['src']}, dst = {item['dst']}")

        return result

if __name__ == '__main__':
    print("测试百度翻译接口")

    baiduTrans = BaiduTrans()
    baiduTrans.Trans('Hello World! This is 1st paragraph.\nThis is 2nd paragraph.')
