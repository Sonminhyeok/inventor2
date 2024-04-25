import pandas as pd
import sys, os
import ast
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.extract_ctr import *
from common.static.config import config
from preprocessing_data.utils import *


def return_record():
    df = pd.read_csv("./../dataset/result.csv")
    input_name = input("name of inventor : ")
    inventor_dicts = df[df["name"]==input_name]
    
    if not inventor_dicts.empty:
        print(inventor_dicts)
        input_applicant = input("select applicant : ")
        for records in inventor_dicts["record"]:
            records = ast.literal_eval(records)
            for record in records:
                if record["applicant"] == input_applicant:
                    print(input_name, record["applicant"], record["start"], record["end"])
                    
    else : 
        print("inventor not found")
    pass
if __name__ == '__main__':
    return_record()