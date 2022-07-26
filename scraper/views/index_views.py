from django.shortcuts import render

# Create your views here.

from django.views import generic
from ..models import Product, Seller

import json
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

def index(request):

    products = Product.objects.filter(user=request.user)

    if request.method == 'POST':
        user = request.user
        user_os = user.userproperty.os
        user_agent = user.userproperty.user_agent

        with open('category.json', 'r') as file:
            category_dict = json.load(file)

        key = request.POST.get('key')
        keyword = request.POST.get('keyword')
        category = request.POST['category']
        # tag1リファクタリング
        if request.POST.get('tag1') == '':
            tag1 = 'すべて'
        else:
            tag1 = request.POST.get('tag1')
        #tag2リファクタリング
        if request.POST.get('tag2')=='':
            tag2 = 'すべて'
        else :
            tag2 = request.POST.get('tag2')

        # category_id作成
        if category == 'すべて':
            category_id = ''
        if tag1 == 'すべて':
            category_id = category_dict[category][tag1]
        else:
            print(tag2)
            tag2_list = tag2.split(' ')
            tag2_list.pop(-1)
            tag2_n = 1
            print(tag2_list)
            for tag2 in tag2_list:
                if tag2_n == 1:
                    category_id = str(category_dict[category][tag1][tag2])
                    tag2_n+=1
                else:
                    category_id = category_id + ',' + str(category_dict[category][tag1][tag2])

        print(category_id)

        # URL作成用
        if keyword == '':
            search_word = ''
        else:
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
        print(search_word)

        CUR_PATH = os.getcwd()
        CHROMEDRIVER = CUR_PATH + '/tools/chromedriver'
        BASE_URL = 'https://jp.mercari.com/search?keyword={0}&order=desc&sort=created_time&status={1}&item_condition_id={2}&category_id={3}&page_token=v1:{4}'
        # 自分のUserAgentを''内に入れる
        USER_AGENT = user_agent

        # Webドライバー作成
        driver_version = '104.0.5112.29'

        options = Options()

        options.add_argument('--user-agent=' + USER_AGENT)
        options.add_argument('--incognito')
        if user_os == 'windows':
            print('windowsです')
            options.binary_location = 'C:/Program Files/Google/Chrome Beta/Application/chrome.exe'
        elif user_os == 'mac':
            print('macです')
            options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'

        chrome_service = service.Service(ChromeDriverManager(version=driver_version).install())

        driver = webdriver.Chrome(
            service = chrome_service,
            options = options
        )

        driver.implicitly_wait(10)

        i = 1
        MAX_PAGE = 1
        url_list = []

        # # 以下クローリング
        sleep(5)
        while i != MAX_PAGE + 1:
            driver.get(BASE_URL.format(search_word, status, item_condition, category_id, i))
            items = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="item-cell"]')

            for item in items:
                item_url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                url_list.append(item_url)
                print(item_url)

            sleep(5)
            i+=1

        for url in url_list:
            driver.get(url)

            product_name = driver.find_element(By.CSS_SELECTOR, 'section > .sticky-outer-wrapper > .sticky-inner-wrapper > div > div >div >div').get_attribute('aria-label')
            product_img = driver.find_element(By.CSS_SELECTOR, 'section > .sticky-outer-wrapper > .sticky-inner-wrapper > div > div >div >div mer-item-thumbnail').get_attribute('src')
            seller_name = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(5) > mer-list > mer-list-item a > mer-user-object').get_attribute('name')
            seller_url = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(5) > mer-list > mer-list-item a').get_attribute('href')
            sold_time = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-of-type(2) > mer-text').text
            shadow_product_price = driver.find_element(By.CSS_SELECTOR, '#item-info mer-price').shadow_root
            product_price = int(shadow_product_price.find_element(By.CSS_SELECTOR, 'span.number').text.replace(',', ''))
            print(seller_name)
            products = Product.objects.create(
                user = user,
                key = key,
                keyword = keyword,
                category = category,
                tag1 = tag1,
                tag2 = tag2,
                product_url = url,
                product_img = product_img,
                product_name = product_name,
                product_price = product_price,
                sold_time = sold_time,
                seller_name = seller_name,
                seller_url = seller_url,
            )
            products.save
            sleep(5)

        driver.quit()
    else:
        user = request.user
    context = {}
    return render(request, 'scraper/index.html', context)