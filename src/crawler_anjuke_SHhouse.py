# Copyright 2022. All Rights Reserved.
# Author: Bruce-Lee-LY
# Date: 23:26:25 on Fri, May 20, 2022
#
# Description: crawler anjuke SHhouse

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


# 60 houses per page
def crawler_anjuke_SHhouse(
        city='beijing',
        district_list=['shijingshan'],
        page=1):
    header = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    csv_path = 'output/anjuke/%s/' % datetime.date.today()
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    for district in district_list:
        csv_name = csv_path + city + '_' + district + '.csv'
        for i in range(page):
            print(
                'city: {}, district: {}, page: {}'.format(
                    city, district, i + 1))
            house_list = []
            if i == 0:
                page_index = ''
            else:
                page_index = 'p%s/' % i
            page_url = 'https://{}.anjuke.com/sale/{}/'.format(
                city, district) + page_index
            page_req = requests.get(page_url, headers=header)
            page_req.encoding = page_req.apparent_encoding
            page_soup = BeautifulSoup(page_req.text, 'html.parser')
            li_list = page_soup.find_all('li', attrs={'class': 'list-item'})
            for li in li_list:
                house = []
                li_soup = BeautifulSoup(str(li), 'html.parser')
                house_a = li_soup.find_all(
                    'a', attrs={'class': 'houseListTitle'})[0]
                house_url = house_a.attrs['href']
                house_req = requests.get(house_url, headers=header)
                house_soup = BeautifulSoup(house_req.text, 'html.parser')
                long_title = house_soup.find_all(
                    'h3', attrs={'class': 'long-title'})[0]
                title = long_title.text.replace(
                    "\n", "").replace(
                    "\t", "").strip()
                info_tag = house_soup.find_all(
                    'span', attrs={'class': 'info-tag'})
                total_price = info_tag[0].text
                type = info_tag[1].text
                area = info_tag[2].text
                houseInfo_detail_item = house_soup.find_all(
                    'li', attrs={'class': 'houseInfo-detail-item'})
                price = houseInfo_detail_item[2].text.replace(
                    "\n", "").replace("\t", "").strip()
                location = houseInfo_detail_item[3].text.replace(
                    "\n", "").replace(
                    "\t", "").replace(
                    " ", "").strip().rstrip('\ue003')
                down_payment = houseInfo_detail_item[5].text.replace(
                    "\n", "").replace("\t", "").strip()
                construction = houseInfo_detail_item[6].text.replace(
                    "\n", "").replace("\t", "").strip()
                orientation = houseInfo_detail_item[7].text.replace(
                    "\n", "").replace("\t", "").strip()
                monthly_offering = houseInfo_detail_item[8].text.replace(
                    "\n", "").replace("\t", "").strip()
                floor = houseInfo_detail_item[10].text.replace(
                    "\n", "").replace("\t", "").strip()
                # elevator = houseInfo_detail_item[13].text.replace(
                #     "\n", "").replace("\t", "").strip()
                # property = houseInfo_detail_item[15].text.replace(
                #     "\n", "").replace("\t", "").strip()
                house.append(title)
                house.append(total_price)
                house.append(type)
                house.append(area)
                house.append(price)
                house.append(location)
                house.append(down_payment)
                house.append(construction)
                house.append(orientation)
                house.append(monthly_offering)
                house.append(floor)
                # house.append(elevator)
                # house.append(property)
                house.append(house_url)
                house_list.append(house)
                print(house)

            house_frame = pd.DataFrame(house_list)
            house_frame.to_csv(
                csv_name,
                mode='a',
                index=False,
                sep=',',
                header=False)


def main():
    crawler_anjuke_SHhouse(
        city='beijing',
        district_list=[
            'shijingshan',
            'haidian',
            'chaoyang',
            'fengtai',
            'dongcheng',
            'xicheng',
            'changping'],
        page=2)


if __name__ == "__main__":
    main()
