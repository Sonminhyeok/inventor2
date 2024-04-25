import pandas as pd
import sys
import numpy as np
import os
import datetime
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from common.static.config import config
from preprocessing_data.extract_ctr import *
from preprocessing_data.utils import *

def load_data(input_df,result_df):
    name_list= input_df["발명자"].to_list()
    applicant_list = input_df["출원인"].to_list()
    date_list = input_df["출원일"].to_list()
    address_list = input_df["주소"].to_list()
    applicant_list_db = convert_to_list(result_df)
    dif_1m = relativedelta(months=1)
    for name, applicant, date, address in zip(name_list, applicant_list, date_list, address_list):
        result="Yes"
        x = str_to_datetime(date)
        
        # applicant_list_db가 비어있는지 확인
        if not applicant_list_db:
            
            applicant_list_db.append({
                "name": name,
                "record": [
                    {
                        "applicant": applicant,
                        "address": address,
                        "start": date,
                        "end": datetime_to_str(x + dif_1m)
                    }
                ]
            })
            continue
        else:
            # applicant_list_db에 name이 존재하는지 확인
            inventor_dicts = [d for d in applicant_list_db if d['name'] == name]
            if not inventor_dicts:
                # name이 없는 경우
                applicant_list_db.append({
                    "name": name,
                    "record": [
                        {
                            "applicant": applicant,
                            "address": address,
                            "start": date,
                            "end": datetime_to_str(x + dif_1m)
                        }
                    ]
                })
                continue
            else:
                no_list=[]
                for inventor_dict in inventor_dicts:
                    for i in range(0,len(inventor_dict["record"])):
                        common_applicant = find_common_item(applicant,inventor_dict["record"][i]["applicant"])
                        if common_applicant != "No":
                            inventor_dict["record"][i]["applicant"]= common_applicant
                            applicant=common_applicant
                    matched_record = next((r for r in inventor_dict['record'] if r['applicant'] == applicant), None)
                    if matched_record:
                        # 같은 출원인인 경우  
                        if x + dif_1m > get_datetime_by_applicant(inventor_dict['record'], applicant, "end"): 
                            matched_record["end"] = datetime_to_str(x + dif_1m) #특허가 단 하나인 경우가 있으므로, 넉넉하게 기간 한 달 추가해줌
                            continue 
                        elif x <= get_datetime_by_applicant(inventor_dict['record'], applicant, "start"):
                            matched_record["start"] = datetime_to_str(x - dif_1m) # 특허가 단 하나인 경우가 있으므로, 넉넉하게 기간 한 달 빼 줌
                            continue
                    else: # 출원인이 다르고, 주소가 같은 경우 조사
                        case2 = next((r for r in inventor_dict['record'] if r['applicant'] != applicant), None)
                        if case2:
                            previous_address = case2["address"] 
                            result = find_common_item(address, previous_address)  #주소가 겹치는 지 판정
                        if result != "No": # 주소가 같은 경우, 동일인으로 판정하고 record에 추가
                            inventor_dict['record'].append({
                                "applicant": applicant,
                                "address": result,
                                "start": date,
                                "end": datetime_to_str(x + dif_1m)
                            })
                            continue
                        else:# 이름은 있지만, 출원인이 다르고 주소도 다른 경우 == 동명이인
                            no_list.append(inventor_dict)
                        if len(no_list)==len(inventor_dicts):
                            # 새로운 출원인인 경우, 기존 레코드에 추가하지 않고 새로운 레코드 생성                       
                            if result=="No":
                                applicant_list_db.append({
                                    "name": name,
                                    "record": [
                                        {
                                            "applicant": applicant,
                                            "address": address,
                                            "start": date,
                                            "end": datetime_to_str(x + dif_1m)
                                        }
                                    ]
                                })
                                
    result_df = pd.DataFrame(columns=["name", "record"])
    result_df["name"] = [d["name"] for d in applicant_list_db]
    # "record" 열을 문자열로 변환하여 저장
    result_df["record"] = [str(d["record"]) for d in applicant_list_db]
    return result_df

def load_foreign_data(input_df,result_df):
    name_list= input_df["발명자"].to_list()
    applicant_list = input_df["출원인"].to_list()
    date_list = input_df["출원일"].to_list()
    address_list = input_df["주소"].to_list()
    applicant_list_db = convert_to_list(result_df)
    dif_1m = relativedelta(months=1)
    for name, applicant, date, address in zip(name_list, applicant_list, date_list, address_list):
        result="Yes"
        x = str_to_datetime(date)
        
        # applicant_list_db가 비어있는지 확인
        if not applicant_list_db:
            
            applicant_list_db.append({
                "name": name,
                "record": [
                    {
                        "applicant": applicant,
                        "address": address,
                        "start": date,
                        "end": datetime_to_str(x + dif_1m)
                    }
                ]
            })
            continue
        else:
            # applicant_list_db에 name이 존재하는지 확인
            inventor_dicts = [d for d in applicant_list_db if d['name'] == name]
            if not inventor_dicts:
                # name이 없는 경우
                applicant_list_db.append({
                    "name": name,
                    "record": [
                        {
                            "applicant": applicant,
                            "address": address,
                            "start": date,
                            "end": datetime_to_str(x + dif_1m)
                        }
                    ]
                })
                continue
            else:
                no_list=[]
                for inventor_dict in inventor_dicts:
                    for i in range(0,len(inventor_dict["record"])):
                        common_applicant = find_common_item(applicant,inventor_dict["record"][i]["applicant"])
                        if common_applicant != "No":
                            inventor_dict["record"][i]["applicant"]= common_applicant
                            applicant=common_applicant
                    matched_record = next((r for r in inventor_dict['record'] if r['applicant'] == applicant), None)
                    if matched_record:
                        # 같은 출원인인 경우  
                        if x + dif_1m > get_datetime_by_applicant(inventor_dict['record'], applicant, "end"): 
                            matched_record["end"] = datetime_to_str(x + dif_1m) #특허가 단 하나인 경우가 있으므로, 넉넉하게 기간 한 달 추가해줌
                            continue 
                        elif x <= get_datetime_by_applicant(inventor_dict['record'], applicant, "start"):
                            matched_record["start"] = datetime_to_str(x - dif_1m) # 특허가 단 하나인 경우가 있으므로, 넉넉하게 기간 한 달 빼 줌
                            continue
                    else: # 출원인이 다르고, 주소가 같은 경우 조사
                        case2 = next((r for r in inventor_dict['record'] if r['applicant'] != applicant), None)
                        if case2:
                            previous_address = case2["address"] 
                            result = find_common_item(address, previous_address)  #주소가 겹치는 지 판정
                        if result != "No": # 주소가 같은 경우, 동일인으로 판정하고 record에 추가
                            inventor_dict['record'].append({
                                "applicant": applicant,
                                "address": result,
                                "start": date,
                                "end": datetime_to_str(x + dif_1m)
                            })
                            continue
                        else:# 이름은 있지만, 출원인이 다르고 주소도 다른 경우 == 동명이인
                            no_list.append(inventor_dict)
                        if len(no_list)==len(inventor_dicts):
                            # 새로운 출원인인 경우, 기존 레코드에 추가하지 않고 새로운 레코드 생성                       
                            if result=="No":
                                applicant_list_db.append({
                                    "name": name,
                                    "record": [
                                        {
                                            "applicant": applicant,
                                            "address": address,
                                            "start": date,
                                            "end": datetime_to_str(x + dif_1m)
                                        }
                                    ]
                                })
                                
    result_df = pd.DataFrame(columns=["name", "record"])
    result_df["name"] = [d["name"] for d in applicant_list_db]
    # "record" 열을 문자열로 변환하여 저장
    result_df["record"] = [str(d["record"]) for d in applicant_list_db]
    return result_df

if __name__ == "__main__":
    df=pd.read_csv("./../dataset/kr_samename.csv")
    df2 = pd.read_csv("./../dataset/result.csv")
    try:
        preprocessed_df=load_data(df,df2)
    except:
        print("error")
    preprocessed_df.to_csv("./../dataset/result_with_foreign.csv",index=False,encoding="utf8")


    
    
    























# # df = pd.read_excel("./../dataset/skey_inv.xlsx")
# # df2 = pd.read_excel("./../dataset/skey_pat.xlsx")
# # df = extract_kr(df)
# # df = merge_to_csv(df,df2,"skey", "출원일")
# # df.to_csv("./../dataset/kr_korean_inv.csv",index=False)





