# Copyright 2022. All Rights Reserved.
# Author: Bruce-Lee-LY
# Date: 23:26:25 on Fri, May 20, 2022
#
# Description: crawler dianyingtiantang magnet

#!/usr/bin/python3
# coding=utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


# 30 movies per page
def crawler_dytt_magnet(kind_list=[1], page=1):
    kind_dict = {
        0: '剧情片',
        1: '喜剧片',
        2: '动作片',
        3: '爱情片',
        4: '科幻片',
        5: '动画片',
        6: '悬疑片',
        7: '惊悚片',
        8: '恐怖片',
        9: '纪录片',
        10: '同性题材电影',
        11: '音乐歌舞题材电影',
        12: '传记片',
        13: '历史片',
        14: '战争片',
        15: '犯罪片',
        16: '奇幻电影',
        17: '冒险电影',
        18: '灾难片',
        19: '武侠片',
        20: '古装片'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    csv_path = 'output/dytt/%s/' % datetime.date.today()
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    for i in kind_list:
        csv_name = csv_path + kind_dict[i] + '.csv'
        for j in range(page):
            print('kind: {}, page: {}'.format(kind_dict[i], j + 1))
            movie_list = []
            if j == 0:
                page_index = 'index'
            else:
                page_index = 'index_' + str(j + 1)
            page_url = 'https://www.dy2018.com/%s/' % i + page_index + '.html'
            page_req = requests.get(page_url, headers=headers)
            page_req.encoding = page_req.apparent_encoding
            page_soup = BeautifulSoup(page_req.text, 'html.parser')
            table_list = page_soup.find_all('table', attrs={'class': 'tbspan'})
            for table in table_list:
                movie = []
                movie_a = table.b.find_all('a')[1]
                movie_name = movie_a["title"]
                movie_url = 'https://www.dy2018.com' + movie_a["href"]
                movie_req = requests.get(movie_url, headers=headers)
                movie_req.encoding = movie_req.apparent_encoding
                movie_soup = BeautifulSoup(movie_req.text, 'html.parser')
                tbody_list = movie_soup.find_all('tbody')
                for tbody in tbody_list:
                    magnet = tbody.a.text
                    if 'magnet:?xt=urn:btih' in magnet:
                        movie.append(movie_name)
                        movie.append(movie_url)
                        movie.append(magnet)
                        print(movie)
                        movie_list.append(movie)
                        break

            movie_frame = pd.DataFrame(movie_list)
            movie_frame.to_csv(
                csv_name,
                mode='a',
                index=False,
                sep=',',
                header=False)


def main():
    crawler_dytt_magnet(
        kind_list=[
            0,
            1,
            2,
            3,
            4,
            6,
            9,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20],
        page=2)


if __name__ == "__main__":
    main()
