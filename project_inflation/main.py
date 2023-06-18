
import warnings
from dataclasses import dataclass,field
from typing import List
# C:\Users\nickl\My_softwares\another\project_inflation\project_inflation
import pandas as pd
import numpy as np
from decimal import *

@dataclass
class WORKED_DATA:
    include_paths: list[str] = field(repr=False,default_factory=list)
    loaded_frames = {}
    @staticmethod
    def make_df(_file_path:str):

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            myexcelfile = pd.read_excel(
                _file_path, engine="openpyxl",
                index_col=None,header=None,names=[f'c{i}'for i in range(7)])

            return myexcelfile
    def df_accumulated(self):

        df_accumulate = pd.concat(
            [WORKED_DATA.make_df(_path) for _path in self.include_paths],
            ignore_index=True)
        return df_accumulate
    @property
    def info(self):
        self.loaded_frames['number'] = len(self.include_paths)


df_raw = WORKED_DATA(
    include_paths= [
        r"C:\Users\nickl\My_softwares\another\project_inflation\project_inflation\docs\receipts.xlsx",
        r"C:\Users\nickl\My_softwares\another\project_inflation\project_inflation\docs\receipts_2.xlsx",
        r"C:\Users\nickl\My_softwares\another\project_inflation\project_inflation\docs\receipts_3.xlsx",
    ])
df_raw.info
# print(df_raw.df_accumulated())
def make_df_store(_data_df:pd.DataFrame):
    store_infor_raw = _data_df.copy()
    store_info_index = store_infor_raw[
        (store_infor_raw['c0'].str.contains('ФН', na=False))
        &
        (store_infor_raw['c1'].str.contains('ФПД', na=False))] \
            .index.tolist()

    store_df = store_infor_raw.iloc[list(map(lambda x: (x+1),store_info_index))]
    new_store_df= store_df.reset_index(drop= True)

    storages_columns = ['FN','OPD',"FD",'storage_name','adres','_date','sum_rub']
    new_store_df.columns=storages_columns

    new_store_df['_index_purch'] = new_store_df.index+base_index+1 # make inexes 1000+1

    new_store_df['sum_rub'] = new_store_df['sum_rub'].apply(Decimal) # convert 'sum_rub' Decimal
    new_store_df['_date'] = pd.to_datetime(new_store_df['_date'])

    return new_store_df