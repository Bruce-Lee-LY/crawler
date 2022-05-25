# Copyright 2022. All Rights Reserved.
# Author: Bruce-Lee-LY
# Date: 23:26:25 on Fri, May 20, 2022
#
# Description: crawler baidu tieba image

#!/usr/bin/python3
# coding=utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import os
import urllib.request
import urllib.parse
import re


def crawler_baidu_tieba_image(tieba_url):
    img_path = 'output/tieba/%s/' % tieba_url.split('/')[-1]
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    page = urllib.request.urlopen(tieba_url)
    html = page.read().decode('utf-8')
    img_re = re.compile(r'src="(.+?\.jpg)" size')
    img_url_list = img_re.findall(html)
    for img_url in img_url_list:
        img_name = img_path + img_url.split('/')[-1]
        urllib.request.urlretrieve(img_url, img_name)
        print(img_name)


def main():
    crawler_baidu_tieba_image('https://tieba.baidu.com/p/4926127781')


if __name__ == "__main__":
    main()
