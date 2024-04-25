import pandas as pd
from soynlp.hangle import levenshtein,jamo_levenshtein ,compose ,decompose, jamo_levenshtein_v2
from geopy.geocoders import Nominatim
import ast
import folium
import webbrowser
from itertools import permutations
geo_local = Nominatim(user_agent='South Korea')

def geocoding_lat(address):
    try:
        geo = geo_local.geocode(address)
        return geo.latitude

    except:
        return 0

#경도 반환 함수
def geocoding_lon(address):
    try:
        geo = geo_local.geocode(address)
        return geo.longitude

    except:
        return 0
def folium_ex(df):
    list1 = df["lat_lon"].to_list()
    name_list = df["name"].to_list()
    map = folium.Map(location=[ast.literal_eval(list1[0])[0], ast.literal_eval(list1[0])[1]], zoom_start=12)
    for latlon, name in zip(list1, name_list):
        latlon = ast.literal_eval(latlon)
        popup = folium.Popup(name,max_width=200)
        folium.CircleMarker(
            [latlon[0], float(latlon[1])],
            radius=10,
            popup=popup,
            color='red',
            fill=True,
            fill_color='#EC4074',
            fill_opacity=0.4,
            parse_html=False,
            ).add_to(map)
    output_file = "map2.html"
    # map = folium.Map(location=[37.5,127.0], zoom_start=15)
    map.save(output_file)
    webbrowser.open_new_tab(output_file) 
def get_geoinfo(df):
    address_list=[]
    for records in df["record"]:
        records = ast.literal_eval(records)
        for record in records:
            address_list.append(record["address"])
    lat_lon_list =[]
    i = len(address_list) 
    i2=0
    for address in address_list:
        i2+=1
        print(f"{i2}/{i}")
        lat = geocoding_lat(address.split(",")[0].split("(")[0].split("|")[0])
        lon = geocoding_lon(address.split(",")[0].split("(")[0].split("|")[0])
        lat_lon_list.append((lat,lon))
    df["lat_lon"]=lat_lon_list
    return df
    
def main():
    df = pd.read_csv("./../dataset/result/langchain_rag_with_trans_0.75.csv")
    name_list = df["names"].to_list()
    search_result_list = df["search_result"].to_list()
    for i in range(len(search_result_list)):
        if search_result_list[i] =="none":
            continue
        search_result_list[i] = search_result_list[i].split("\\")[0].split(":")[1]
        search_result_list[i] = search_result_list[i].replace(",","")
        search_result_list[i] = search_result_list[i].split(" ")
        search_result_list[i] = list(permutations(search_result_list[i], len(search_result_list[i])))
    for name, result_list in zip(name_list,search_result_list):
        # print(result_list)
        if result_list =="none":
            continue
        min = 10
        for result in result_list:
            result = " ".join(result)

            score = jamo_levenshtein(result , name)
            if score < min:
                temp_name = result
                min = score
        print(min,name ,temp_name )
if __name__ == '__main__':
    main()
# print(levenshtein(s1, s2))
# print(jamo_levenshtein(s1,s2))
