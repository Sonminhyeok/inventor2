import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.utils import *
from preprocessing_data.extract_ctr import *
from common.static.config import config
import ast
from openai import OpenAI
import anthropic
import time
# def get_translated_openai(client, sys_prompt,user_prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": sys_prompt},
#             {"role": "user", "content": user_prompt},
#         ]
#     )
#     return response.choices[0].message.content

# def example2():
#     sys_prompt = """
#         I'll give you a name and country code, and you should convert name into korean.
#         Don't believe country code, is can be wrong in probability of 10 percent.
#         Remember that if country code is korea, most of korean name is executed with three letters.
#         For example, [
#             Input: 'Ju Hwi LEE', "kr",  Output: '이주휘'.
#             Input: 'Tai, Yongmin', "kr",  Output:'태용민'.
#             Input: 'SHARMA, Manali', "us",  Output:'샤르마, 마날리'.]
#         don't use comma.
#         Never answer anything else except name.
#         For example, don't say 'korean name is~, First ~'

#         Let's think step by step
#         """
#     user_prompt ="""
#         Given name is [NAME] and country code is [CTR].
#         """
#     model = "gpt-3.5-turbo"
#     openai_api_key = config['KEY']['openai_api_key']
#     client= OpenAI(api_key=openai_api_key)
#     df = pd.read_csv("./../dataset/for_inv.csv")
#     df = df.head(20)
#     name_list = df["발명자"].to_list()
#     applicant_list = df["출원인"].to_list()
#     national_list = df["발명자국적"]
#     lang_code_list=df["fasttext_result"].to_list()
#     result_list =[]
#     for name, applicant, national,lang_code in zip(name_list, applicant_list, national_list,lang_code_list):
#         names = name.split("|")
#         nationals= national.split("|")
#         temp_list=[]
#         for inventor_name, inventor_national in zip(names,nationals):
#             result= get_translated_openai(client, sys_prompt, user_prompt.replace("[NAME]", inventor_name).replace("[CTR]", inventor_national))
#             print(result)
#             temp_list.append(result)
#         result = "|".join(temp_list)
#         result_list.append(result)
#     df["translated"]=result_list
#     df.to_csv("./../dataset/for_inv_trans.csv",index=False)

def get_translated_cluade(client, prompt):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        # model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        messages=
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text


# def lang_translator(df):
#     prompt = """
#         I'll give you a name and country code, and you should convert name into korean.
#         Don't believe country code, is can be wrong in probability of 10 percent.
#         Remember that if country code is korea, most of korean name is executed with three letters.
#         For example, [
#             Input: 'Ju Hwi LEE', "kr",  Output: '이주휘'.
#             Input: 'Tai, Yongmin', "kr",  Output:'태용민'.
#             Input: 'SHARMA, Manali', "us",  Output:'샤르마, 마날리'.]
#         don't use comma.
#         Never answer anything else except name.
#         For example, don't say 'korean name is~, First ~'
#         Given name is [NAME] and country code is [CTR].
#         Let's think step by step
#         """
#     client = anthropic.Anthropic(
#         api_key=config['KEY']['anthropic_api_key'],
#     )
#     df = pd.read_csv("./../dataset/for_inv.csv")
#     name_list = df["발명자"].to_list()
#     applicant_list = df["출원인"].to_list()
#     national_list = df["발명자국적"]
#     lang_code_list=df["fasttext_result"].to_list()
#     result_list =[]
#     for name, applicant, national,lang_code in zip(name_list, applicant_list, national_list,lang_code_list):
#         names = name.split("|")
#         nationals= national.split("|")
#         temp_list=[]
#         for inventor_name, inventor_national in zip(names,nationals):
#             # result= get_translated_openai(client, prompt.replace("[NAME]", inventor_name).replace("[CTR]", inventor_national))
#             result= get_translated_cluade(client, prompt.replace("[NAME]", inventor_name).replace("[CTR]", inventor_national))
#             time.sleep(12)
#             print(result)
#             temp_list.append(result)
#         result = "|".join(temp_list)
#         result_list.append(result)
#     df["translated"]=result_list
#     # df.to_csv(result_path,index=False)
#     return df
def lang_translator(df):
    prompt = """
        I'll give you a name and country code, and you should convert name into korean.
        Don't believe country code, is can be wrong in probability of 10 percent.
        Remember that if country code is korea, most of korean name is executed with three letters.
        For example, [
            Input: 'Ju Hwi LEE', "kr",  Output: '이주휘'.
            Input: 'Tai, Yongmin', "kr",  Output:'태용민'.
            Input: 'SHARMA, Manali', "us",  Output:'샤르마, 마날리'.]
        don't use comma.
        Never answer anything else except name.
        For example, don't say 'korean name is~, First ~'
        Given name is [NAME] and country code is [CTR].
        Let's think step by step
        """
    client = anthropic.Anthropic(
        api_key=config['KEY']['anthropic_api_key'],
    )
    df = pd.read_csv("./../dataset/for_inv.csv")
    name_list = df["발명자"].to_list()
    applicant_list = df["출원인"].to_list()
    national_list = df["발명자국적"]
    lang_code_list=df["fasttext_result"].to_list()
    result_list =[]
    for name, applicant, national,lang_code in zip(name_list, applicant_list, national_list,lang_code_list):
        names = name.split("|")
        nationals= national.split("|")
        # for inventor_name, inventor_national in zip(names,nationals):
        result = get_translated_cluade(client, prompt.replace("[NAME]", str(names)).replace("[CTR]", str(nationals)) )
        print(result)
        time.sleep(12)
        result_list.append(result)
    df["translated"]=result_list
    # df.to_csv(result_path,index=False)
    return df
if __name__ == "__main__":
    # example1()
    df=  pd.read_csv("./../dataset/result.csv")
    translated_df = lang_translator(df)
    translated_df.to_csv("./../dataset/for_inv_trans_claude.csv",index=False)
    # list1 = df.to_list()
    # print(list1)












