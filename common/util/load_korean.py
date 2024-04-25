import ast
import sys
import subprocess

from common.util.extract_ctr import *
from dateutil.relativedelta import relativedelta

import os
from common.util import how_long
from common.static.log import logger
from common.static.global_variable import GlobalVariable as gv
datamanager = DataManager()

class Record():
    # class Record:
    #     def __init__(self, name, applicant, address, date):
    #         self.name = name
    #         self.records = [(applicant, address, date, datamanager.datetime_to_str(datamanager.str_to_datetime(date) + relativedelta(months=1)))]
    #
    #     def add_record(self, applicant, address, date):
    #         self.records.append((applicant, address, date))
    def __init__(self, name: str, applicant: str, address: str, date):

        self.name = name
        self.applicant = applicant
        self.address = address
        self.start = date
        self.end = datamanager.datetime_to_str(datamanager.str_to_datetime(date) + relativedelta(months=1))
    def add_one_month(self):

        self.end= datamanager.datetime_to_str(datamanager.str_to_datetime(self.end) + relativedelta(months=1))
    def minus_one_month(self):
        self.start = datamanager.datetime_to_str(datamanager.str_to_datetime(self.end) - relativedelta(months=1))
    def __str__(self):
        return f"Record(Name: {self.name}, Applicant: {self.applicant}, Address: {self.address}, Start: {self.start}, End: {self.end})"


class DataHandler():
    def __init__(self, file_name: str):
        self.table_path = os.path.join(gv.ROOT_PATH, 'dataset', 'son', file_name)
        self.df = pd.read_csv(self.table_path)
        self.records = self.load_data()

    @how_long
    def load_data(self):
        df = self.df
        record_list = []
        for index, row in df.iterrows():
            record = Record(name=str(df["발명자"].iloc[index]), applicant=df["출원인"].iloc[index],
                            address=df["주소"].iloc[index],
                            date=df["출원일"].iloc[index])
            record_list.append(record)
        return record_list

    def search_data(self, target_record, target_col):
        searched_data = [d for d in self.records if getattr(d, target_col) == getattr(target_record, target_col)]
        return searched_data

    def add_data(self, record):
        self.records.append(record)
        # self.records.sort(key=lambda x: x.name)
        pass

    def update_data(self, record):
        target_record = self.search_data(record, "name")
        if target_record is not None:
            for target in target_record:
                self.delete_data(target)

            for i in range(0,len(target_record)):
                if record.name == target_record[i].name:
                    if record.applicant == target_record[i].applicant:
                        print(target_record[i].applicant)
                        if target_record[i].start > record.start:
                            target_record[i].start = record.start
                        if target_record[i].end < record.end:
                            target_record[i].end = record.end
                            target_record[i].add_one_month()
                        break
                    elif record.address == target_record[i].address:
                        #TODO: address가 같은데, applicant가 다른 경우. 이런 경우는 이직을 한 경우. 따라서 record에 추가해서 올려야함. 그런데? 지금 record는 리스트 형태가 아님.

                        if target_record[i].start > record.start:
                            target_record[i].start = record.start
                            target_record[i].minus_one_month()
                        if target_record[i].end < record.end:
                            target_record[i].end = record.end
                            target_record[i].add_one_month()
                        break
                    else:
                        target_record.append(record)

            for target in target_record:
                self.add_data(target)

        pass

    def delete_data(self, record):
        searched_record_list = self.search_data(record, "name")
        if searched_record_list is not None:
            for record in searched_record_list:
                self.records.remove(record)

    def get_data(self):
        return self.records

    def save_data(self, record, number):
        pd.DataFrame(self.records).to_csv(os.path.join(gv.ROOT_PATH, 'dataset', 'son', 'result', f'save_{number}.csv'),
                                          index=False)


if __name__ == '__main__':
    file_name = "kr_samename.csv"
    data = DataHandler(file_name=file_name)
    search_data = data.search_data(Record(name="테스트", applicant="테스트", address="테스트", date="2024-04-25"), "name")
    data.update_data(Record(name="테스트", applicant="테스트", address="테스트", date="2025-05-01"))
    print(data.get_data()[-2])

    pass
