"""" 
Just an example of simple web scraping.
Webスクレイピングによる店舗住所取得の例です。
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


"""
Rondom company with many shops is set as an example.
店舗の多い会社の例として、ほけんの窓口を挙げます。他の会社でも基本的には同じです。
Homepage here : https://www.hokennomadoguchi.com/shop-list/
"""

urlName = "https://www.hokennomadoguchi.com/shop-list/"
url = requests.get(urlName)
soup = BeautifulSoup(url.content, "html.parser")


shop_name_list = []
address_list = []
# select finds class and id. selectでクラスやidを探します。
for elem in soup.select(".shop-link"):
    # find finds first tag appears. findでは最初に表れる対応するタグを探します。
    # get finds attributes. getは属性（アトリビュート）を取得します。
    shop_url = "https://www.hokennomadoguchi.com" + elem.find("a").get("href")
    # contents breakdowns tags. contentsはタグをブレークダウンして、タグの部分やアトリビュートが選択できるようにします。
    shop_name = elem.find("a").select(".shop_name")[0].contents[0]
    print("--- "+ shop_name +" ---")
    url = requests.get(shop_url)
    soup_shop = BeautifulSoup(url.content, "html.parser")
    address = soup_shop.select(".item2")[0].contents[2].replace(" ","").replace("\u3000","").replace("\r","").replace("\n","")
    print(address)

    shop_name_list.append(shop_name)
    address_list.append(address)
    
    
df_madoguchi = pd.DataFrame([shop_name_list,address_list]).T
df_madoguchi.columns=["shop_name", "address"]

df_madoguchi.to_csv("madoguchi_address.csv", encoding='utf_8_sig')
