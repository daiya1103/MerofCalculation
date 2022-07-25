from django.shortcuts import render

# Create your views here.

from django.views import generic
from ..models import Product

import json
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import platform
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from collections import Counter
import re

def index(request):

    products = Product.objects.filter(user=request.user)

    if request.method == 'POST':

        with open('category.json', 'r') as file:
            category_dict = json.load(file)

        print(category_dict)

        category = request.POST['category']
        tag1 = request.POST['tag1']
        if request.POST['tag2']=='':
            tag2 = 'すべて'
        else :
            tag2 = request.POST['tag2']
        keyword = request.POST.get('keyword')
        user_agent = request.POST.get('agent')

        CUR_PATH = os.getcwd()
        CHROMEDRIVER = CUR_PATH + '/tools/chromedriver'
        BASE_URL = 'https://jp.mercari.com/search?keyword={0}&order=desc&sort=created_time&status={1}&item_condition_id={2}&t1_category_id={3}&category_id={4}&page_token=v1:{5}'
        # 自分のUserAgentを''内に入れる
        USER_AGENT = user_agent

        # Webドライバー作成
        options = webdriver.ChromeOptions()

        options.add_argument('--user-agent=' + USER_AGENT)
        options.add_argument('--incognito')

        chrome_service = service.Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(
            service = chrome_service,
            options = options
        )

        driver.implicitly_wait(10)

        # URL作成用
        search_word = keyword.split()
        n=1
        for word in search_word:
            if n == 1:
                search_word = word
                n+=1
            else:
                search_word = search_word + '+' + word
        status = 'sold_out'
        item_condition = 1
        t1_category_id = 3
        category_item_data = ['282', '283', '284']
        category_n=1
        for num in category_item_data:
            if category_n == 1:
                category_id = num
                category_n+=1
            else:
                category_id = category_id + ',' + num


        i = 1
        MAX_PAGE = 5
        item_data = []

        # # 以下クローリング
        sleep(5)
        while i != MAX_PAGE + 1:
            driver.get(BASE_URL.format(search_word, status, item_condition, t1_category_id, category_id, i+1))
            items = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="item-cell"]')

            for item in items:
                item_url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                item_name = item.find_element(By.CSS_SELECTOR, 'mer-item-thumbnail').get_attribute('item-name')

                shadow_item_price = item.find_element(By.CSS_SELECTOR, 'mer-item-thumbnail').shadow_root
                item_price = shadow_item_price\
                    .find_element(By.CSS_SELECTOR, 'figure div.price-container mer-price')\
                        .get_attribute('value')

                item_data.append({
                    '商品名': item_name,
                    'URL': item_url,
                    '価格': int(item_price),
                })
                print(item_url)

            sleep(5)
            i+=1

        # seller_url_list = []
        # seller_data_list = []
        # for data in item_data:
        #     item_url = data['URL']
        #     driver.get(item_url)

        #     seller_name = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(5) > mer-list > mer-list-item a > mer-user-object').get_attribute('name')
        #     seller_url = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(5) > mer-list > mer-list-item a').get_attribute('href')
        #     time = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(2) > mer-text').text

        #     data['セラー'] = seller_name
        #     data['セラーURL'] = seller_url
        #     data['出品時間'] = time
        #     seller_data_list.append((
        #         seller_name,
        #         seller_url,
        #     ))
        #     print(seller_name)
        #     sleep(5)

        # count_seller = Counter(seller_data_list)
        # sellers = count_seller.keys()
        # seller_data = [
        #     {
        #         'セラー': seller[0],
        #         'セラーURL': seller[1],
        #         '出現回数': count_seller[seller[0], seller[1]],
        #     }
        #     for seller in sellers
        # ]

        # for seller in seller_data:
        #     seller_revenue = 0
        #     for item in item_data:
        #         if seller['セラー'] == item['セラー']:
        #             seller_revenue = seller_revenue + item['価格']
        #         else:
        #             continue
        #     seller['セラー総売上'] = seller_revenue

        # item_df = pd.DataFrame(item_data)
        # seller_df = pd.DataFrame(seller_data).sort_values('出現回数', ascending=False)



        # with pd.ExcelWriter(CUR_PATH+'/data/kids.xlsx') as writer:
        #     item_df.to_excel(writer, sheet_name='商品リスト', index=None)
        #     seller_df.to_excel(writer, sheet_name='出品者リスト', index=None)

        driver.quit()
    else:
        user = request.user
    context = {}
    return render(request, 'scraper/index.html', context)