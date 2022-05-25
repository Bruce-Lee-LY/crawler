# Copyright 2022. All Rights Reserved.
# Author: Bruce-Lee-LY
# Date: 23:26:25 on Fri, May 20, 2022
#
# Description: crawler baidu image

#!/usr/bin/python3
# coding=utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import os
import requests
import urllib.request
import urllib.parse
import re


# 30 pictures per page
def crawler_baidu_image(keyword='car', page=1):
    keyword_quote = urllib.parse.quote(keyword)
    page_headers = {
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    img_re = re.compile('"thumbURL":"(.*?)",')
    img_path = 'output/baidu/%s/' % keyword
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    for i in range(page):
        page_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={}&pn={}&rn=30&gsm=1e&1541136876386='.format(
            keyword_quote,
            keyword_quote,
            i *
            30)
        page_req = requests.get(page_url, headers=page_headers)
        page_req.encoding = page_req.apparent_encoding
        img_url_list = img_re.findall(page_req.text)
        for img_url in img_url_list:
            img_headers = {
                'Referer': img_url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
            img_req = requests.get(img_url, headers=img_headers)
            img_req.encoding = img_req.apparent_encoding
            img_name = img_path + img_url.split('/')[-1]
            with open(img_name, 'wb') as fw:
                fw.write(img_req.content)
                print(img_name)


def main():
    crawler_baidu_image(keyword='dog', page=1)


if __name__ == "__main__":
    main()
