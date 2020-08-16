import json
import pandas as pd
import requests
import time


def progress_decolator(input_function):
    """Decolator to print * to show progress"""
    def return_function(*args, **kwargs):
        print("*", end="")
        result = input_function(*args, **kwargs)
        return result
    return return_function


def get_distance_API(lat1, lng1, lat2, lng2):
    """ Get distance between two points described with latitute and longitude.
    Details of the API can be found here: https://vldb.gsi.go.jp/sokuchi/surveycalc/api_help.html
    Validate the result using this web app : https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2stf.html

    Input : latitute and longitude of two points (float)
        eg) 35.6585769, 139.7454506, 35.710256, 139.8107946

    Output : distance of input two points with kilo meter unit (float)
        eg) 8.237
    """
    url = "http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2st_calc.pl?latitude1={}&longitude1={}&latitude2={}&longitude2={}&ellipsoid=bessel&outputType=json".format(lat1,lng1,lat2,lng2)
    i_count = 0
    while i_count <= 10:
        result = requests.get(url)
        status_code = result.status_code
        if status_code == 200:
            break
        i_count += 1    
        time.sleep(2)
        print("retry : {}".format(i_count+1),end="")
        
    result_json = json.loads(result.text)
    distance = "0" + result_json["OutputData"]["geoLength"] 
    if distance == "0":
        print("error here")
        print(url)
        print(result)
        print(result_json)
    return round(float(distance)/1000, 3)

def get_distance_locally(lat_a, lon_a,lat_b, lon_b):
    """
    Credit : https://qiita.com/damyarou/items/9cb633e844c78307134a
    """
    ra=6378.140  # equatorial radius (km)
    rb=6356.755  # polar radius (km)
    F=(ra-rb)/ra # flattening of the earth
    rad_lat_a=np.radians(lat_a)
    rad_lon_a=np.radians(lon_a)
    rad_lat_b=np.radians(lat_b)
    rad_lon_b=np.radians(lon_b)
    pa=np.arctan(rb/ra*np.tan(rad_lat_a))
    pb=np.arctan(rb/ra*np.tan(rad_lat_b))
    xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
    c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
    c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
    dr=F/8*(c1-c2)
    rho=ra*(xx+dr)
    return rho

@progress_decolator
def get_distance(lat1, lng1, lat2, lng2, method=0):
    if method == 0:
        return_distance = get_distance_API(lat1, lng1, lat2, lng2)
    else: 
        return_distance = get_distance_locally(lat1, lng1, lat2, lng2)
    return return_distance 


def create_matrix(n_row, n_col):
    """Create matrix filled with nan in decided size
    
    Input : n_row(int), n_col(int)
    Output : dataframe
    """
    
    matrix = pd.DataFrame(index=range(n_row), columns=range(n_col))
    return matrix



# main here

df1 = pd.read_csv("PATH1.csv")
df2 = pd.read_csv("PATH2.csv")

matrix = create_matrix(len(df1), len(df2))

for i in range(len(df1)):
    for j in range(len(df2)):
        distance = get_distance(df1.loc[i,"latitude"], 
                                df1.loc[i,"longitude"], 
                                df2.loc[j, "latitude"], 
                                df2.loc[j, "longitude"],
                               method = 0)
        if distance == 0:
            # if distance equal 0, that is most probably wrong. check what is the problem.
            # distanceが0の場合、問題が発生していることが多いです。そのため確認を行ってください。
            print(df1[i])
            print(df2[j])
        matrix.iloc[i,j] = distance
        
matrix.to_csv("output.csv", encoding='utf_8_sig')

# if you want to decolate output with headings, run the followings
# 以下はヘッダーの追加です。任意で実行してください。

col_expanded = pd.concat([df1[["name","address"]],matrix], axis = "columns")
df_head = pd.DataFrame([[""]*2,[""]*2],columns=["name","address"])
df_head = pd.concat([df_head , df2[["name","address"]]], ignore_index=True).T.reset_index(drop=True)
df_head.columns = col_expanded.columns
df_head.index = ["name", "address"]
df_expanded = pd.concat([df_head, col_expanded])
df_expanded.to_csv("output_with_header.csv", encoding='utf_8_sig')
