import csv
import glob
import os

import pandas as pd


def unique_csv(path: str):
    """
    房屋信息去重
    """
    df = pd.read_csv('source/' + path)
    df_unique = df.drop_duplicates(subset='url')
    df_unique.to_csv('./unique/unique_' + path, index=False)


def all_csv(path: str):
    """
    将去重后的房屋信息合并到一个csv文件中
    """
    csv_files = glob.glob(os.path.join(path, '*.csv'))
    all_data = pd.DataFrame()
    for file in csv_files:
        data = pd.read_csv(file)
        all_data = pd.concat([all_data, data], ignore_index=True)
    all_data.to_csv('all.csv', index=False)


def process_csv(path: str):
    """
    处理房屋信息
    """
    data = pd.read_csv(path)

    # 根据条件筛选行
    condition = ((data['price'] < 10000) & (data['area'] > 1000)) | (
        data['price'] <= 0) | (data['area'] <= 0) | (data['room_type'] == '未知')

    filtered_data = data.drop(data[condition].index)
    filtered_data.to_csv('all.csv', index=False)


unique_csv('bj_rent_house.csv')
unique_csv('sh_rent_house.csv')
unique_csv('gz_rent_house.csv')
unique_csv('sz_rent_house.csv')
unique_csv('zmd_rent_house.csv')

all_csv('unique')

process_csv('all.csv')
