import re
import pandas as pd
import datetime
import pandas as pd


class DataManager:
    def __init__(self):
        pass
    def get_data_by_name(self, name, col):
        filtered_df = self.df[self.df['name'] == name]
        return filtered_df[col].values

    @staticmethod
    def str_to_datetime(date_str: str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    @staticmethod
    def datetime_to_str(date: datetime.datetime):
        return datetime.datetime.strftime(date, "%Y-%m-%d")

# def get_datetime_by_name(df,name,time="start"):
#     return datetime.datetime.strptime(list(filter(lambda item : item['name'] == name, df))[0][time],"%Y-%m-%d")
def get_datetime_by_applicant(record_list, applicant, time):
    for record in record_list:
        if record['applicant'] == applicant:
            return datetime.datetime.strptime(record[time], "%Y-%m-%d")
    return None


def find_common_item(address, previous_address):
    address_list=address.split("|")
    previous_address_list=previous_address.split("|")
    common_address_list=[]
    
    for address1 in address_list:
        for address2 in previous_address_list:
            if address1 == address2:
                common_address_list.append(address1)
    if common_address_list:
        common_address= "|".join(common_address_list)
        return common_address
    else:
        return "No"

def convert_to_list(df):
    import ast
    # df=  pd.read_csv("./../dataset/result.csv")
    list1 = df["name"].to_list()
    list2 = df["record"].to_list()
    list3 = []
    for name, record in zip(list1,list2):
        list3.append(dict({"name":name, "record":ast.literal_eval(record)}))
    return list3

def split_same_notsame():
    df = pd.read_csv("./../dataset/result.csv")
    df3 = pd.read_csv("./../dataset/for_inv_trans_claude_sonnet_explode.csv")
    name_list = df["name"].to_list()
    df_list = []
    df_filtered = pd.DataFrame(columns=df3.columns)

    # Iterate through df3 and filter data
    for index, row in df3.iterrows():
        if row["translated"] in name_list:
            # If name is in name_list, add it to df_filtered
            df_filtered = df_filtered._append(row)
        else:
            # If name is not in name_list, add it to df_list
            df_list.append(row)

    # Save the filtered dataframes to CSV
    df_filtered.to_csv("./../dataset/for_inv_trans_claude_sonnet_same.csv", index=False)
    pd.DataFrame(df_list).to_csv("./../dataset/for_inv_trans_claude_sonnet_withoutsame.csv", index=False)

    
def extract_kr(df):
    korean_pattern = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    df["출원인국적"]= df["출원인국적"].fillna("")
    kr_df = df[df["출원인국적"].str.contains("KR")]
    kr_korean_df = kr_df[kr_df["발명자"].apply(lambda x: korean_pattern.search(x) is not None)]
    return kr_korean_df
def extract_not_kr(df):
    korean_pattern = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    df["출원인국적"]= df["출원인국적"].fillna("")
    kr_df = df[df["출원인국적"].str.contains("KR")]
    kr_korean_df = kr_df[kr_df["발명자"].apply(lambda x: korean_pattern.search(x) is None)]
    return kr_korean_df
def extract_samename(df, column):
    exploded_df = df.assign(발명자=df[column].str.split("|")).explode(column, ignore_index=True)
    duplicate_names = exploded_df[exploded_df.duplicated(subset=[column], keep=False)]
    duplicate_names=duplicate_names.sort_values(by=column)
    return duplicate_names
def merge_to_csv(df1,df2,overlap_col, target_col):
    common_skeys = df2[df2[overlap_col].isin(df1[overlap_col])]
    merged_df = pd.merge(df1, df2, on=overlap_col, how='left')

    # 'skey'가 일치하는 행에 '출원일' 열 추가
    merged_df[target_col] = merged_df[target_col].fillna(merged_df[target_col])
    sorted_df = merged_df.sort_values(by='출원일')
    return sorted_df
def explode_split(df,column):
    df[column] = df[column].str.split('|')
    split_df=df.explode(column)
    return split_df

if __name__ == "__main__":
    # df=pd.read_csv("./../dataset/for_inv.csv")
    # df.to_csv("./../dataset/example2.csv",index=False)
    pass