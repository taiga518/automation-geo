import json
import pandas as pd
import requests
import time

API_key = "XXXXX"
"""    
APIキーはご自身で取得する必要があるのでご注意ください。
個人的な使用頻度では料金を請求されないと思いますが、料金表はよく確認してください。
API key needs to be set to use google geocode API. Follow the guidance here :
https://developers.google.com/maps/documentation/geocoding/overview
"""


def start_end_decolator(input_function):
    """Decolator to print start and end"""
    def return_function(*args, **kwargs):
        print("\n--------------start--------------")
        result = input_function(*args, **kwargs)
        print("\n---------------end---------------")
        return result
    return return_function

def progress_decolator(input_function):
    """Decolator to print * to show progress"""
    def return_function(*args, **kwargs):
        print("*", end="")
        result = input_function(*args, **kwargs)
        return result
    return return_function

@progress_decolator
def get_location(address):
    """ 
    Googleのgeocodeを使って、住所から経度緯度を取得します。
    
    Get latitude and longitude using google geocode API.
    API key needs to be set to use google geocode API. Follow the guidance here : 
    https://developers.google.com/maps/documentation/geocoding/overview
    Check billing here: https://console.cloud.google.com/google/maps-apis/overview
    
    Input : address as text
        eg) "東京都港区芝公園４丁目２−8"
        
    Output : tupple of address(text), latitude(float), longitude(float)
        eg) ('4-chōme-2-8 Shibakōen, Minato City, Tōkyō-to 105-0011, Japan', 35.6585769, 139.7454506)
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=+"+address+"&key="+API_key
    result = requests.get(url)
    result_json = json.loads(result.text)
    formatted_address = result_json["results"][0]["formatted_address"]
    lat, lng = result_json["results"][0]["geometry"]["location"].values()
    return (formatted_address, lat, lng)


@start_end_decolator    
def add_location_info(input_df):
    """
    複数の住所のリストから、上記のget_location関数を使って経度緯度のリストを取得します。
    
    Get lists of location information using get_location function.
    
    Input : dataframe with address information named address
    Output : dataframe with formatted_address, latitute, longitude columns
    """    
    
    formatted_address_list = []
    lat_list = []
    lng_list = []

    for i_row in range(len(input_df)):
        formatted_address, lat, lng = get_location(input_df.loc[i_row,"address"])
        formatted_address_list.append(formatted_address)
        lat_list.append(lat)
        lng_list.append(lng)
    
    output_df = input_df
    output_df["formatted_address"] = formatted_address_list
    output_df["latitude"] = lat_list
    output_df["longitude"] = lng_list
    return output_df



### main here

df = pd.read_csv("PATH.csv")
df = df[["name","address"]]
df_loc = add_location_info(df)
df_loc.to_csv("output.csv")
