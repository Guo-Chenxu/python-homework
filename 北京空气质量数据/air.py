import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def process_humi_pres_temp(csv_file, save_path: str):
    data = pd.read_csv(csv_file, dtype=str)

    # 提取"HUMI"、"PRES"和"TEMP"列的数据
    humi_data = data["HUMI"].astype(float)
    pres_data = data["PRES"].astype(float)
    temp_data = data["TEMP"].astype(float)

    # 计算每列数据的均值和标准差
    humi_mean = np.mean(humi_data)
    humi_std = np.std(humi_data)

    pres_mean = np.mean(pres_data)
    pres_std = np.std(pres_data)

    temp_mean = np.mean(temp_data)
    temp_std = np.std(temp_data)

    # 处理湿度数据
    for i in range(len(humi_data)):
        if humi_data[i] > humi_mean + 3 * humi_std:
            humi_data[i] = humi_mean + 3 * humi_std

        if np.isnan(humi_data[i]):
            prev_val = humi_data[i - 1]
            next_val = humi_data[i + 1]
            j = 1

            while np.isnan(prev_val):
                prev_val = humi_data[i - j]
                j += 1

            j = 1
            while np.isnan(next_val):
                next_val = humi_data[i + j]
                j += 1

            humi_data[i] = np.interp(i, [i - j, i + j], [prev_val, next_val])

    # 处理气压数据
    for i in range(len(pres_data)):
        if pres_data[i] > pres_mean + 3 * pres_std:
            pres_data[i] = pres_mean + 3 * pres_std

        if np.isnan(pres_data[i]):
            prev_val = pres_data[i - 1]
            next_val = pres_data[i + 1]
            j = 1

            while np.isnan(prev_val):
                prev_val = pres_data[i - j]
                j += 1

            j = 1
            while np.isnan(next_val):
                next_val = pres_data[i + j]
                j += 1

            pres_data[i] = np.interp(i, [i - j, i + j], [prev_val, next_val])

    # 处理温度数据
    for i in range(len(temp_data)):
        if temp_data[i] > temp_mean + 3 * temp_std:
            temp_data[i] = temp_mean + 3 * temp_std

        if np.isnan(temp_data[i]):
            prev_val = temp_data[i - 1]
            next_val = temp_data[i + 1]
            j = 1

            while np.isnan(prev_val):
                prev_val = temp_data[i - j]
                j += 1

            j = 1
            while np.isnan(next_val):
                next_val = temp_data[i + j]
                j += 1

            temp_data[i] = np.interp(i, [i - j, i + j], [prev_val, next_val])

    # 保存处理后的数据
    data["HUMI"] = humi_data
    data["PRES"] = pres_data
    data["TEMP"] = temp_data
    data.to_csv(save_path, index=False)


def process_pm_data(data_path, save_path: str):
    data = pd.read_csv(data_path)

    # 列名
    columns = ["PM_Dongsi", "PM_Dongsihuan", "PM_Nongzhanguan", "PM_US Post"]

    for column in columns:
        # 处理超过500的数据
        data[column] = np.where(data[column] > 500, 500, data[column])
        # 处理缺失值插值
        data[column] = data[column].interpolate()

    data.to_csv(save_path, index=False)


def process_cbwd_data(data_path, save_path: str):
    data = pd.read_csv(data_path)

    # 处理"cbwd"列中值为"cv"的单元格，用后项数据填充
    data["cbwd"] = data["cbwd"].replace("cv", np.nan).ffill()

    data.to_csv(save_path, index=False)


def normalize_and_scatter(data_path, save_path: str):
    plt.rcParams["font.family"] = 'Microsoft YaHei'
    data = pd.read_csv(data_path)

    # 选择需要归一化的列
    columns = ["DEWP", "TEMP"]

    # 0-1 归一化
    minmax_scaler = MinMaxScaler()
    data_minmax = minmax_scaler.fit_transform(data[columns])

    # Z-Score 归一化
    zscore_scaler = StandardScaler()
    data_zscore = zscore_scaler.fit_transform(data[columns])

    # 创建散点图
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("DEWP 和 TEMP 0-1 归一化和 Z-Score 归一化散点图及原图")

    # 绘制0-1归一化散点图
    axes[0, 0].scatter(data_minmax[:, 0], data_minmax[:, 1], s=5, alpha=0.5)
    axes[0, 0].set_title("0-1 归一化")
    axes[0, 0].set_xlabel("DEWP")
    axes[0, 0].set_ylabel("TEMP")

    # 绘制Z-Score归一化散点图
    axes[0, 1].scatter(data_zscore[:, 0], data_zscore[:, 1], s=5, alpha=0.5)
    axes[0, 1].set_title("Z-Score 归一化")
    axes[0, 1].set_xlabel("DEWP")
    axes[0, 1].set_ylabel("TEMP")

    # 绘制原始数据散点图
    axes[1, 0].scatter(data[columns[0]], data[columns[1]], s=5, alpha=0.5)
    axes[1, 0].set_title("原始数据")
    axes[1, 0].set_xlabel("DEWP")
    axes[1, 0].set_ylabel("TEMP")

    # 移除多余的子图
    fig.delaxes(axes[1, 1])

    # 调整子图间距
    plt.tight_layout()
    plt.savefig(save_path)


def calculate_air_quality(data_path, daily_path, counts_path: str):
    data = pd.read_csv(data_path)

    # 根据日期（year, month, day）进行分组，计算每天空气质量数据的平均值
    daily_average = data.groupby(['year', 'month', 'day'])[
        ['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].mean()
    daily_average['AirQuality'] = daily_average.mean(axis=1)

    # 创建一个新的"AQI"列，离散化为AQI级别
    daily_average['AQI'] = pd.cut(daily_average['AirQuality'], bins=[0, 50, 100, 150, 200, 300, float('inf')],
                                  labels=['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染'])
    daily_average.to_csv(daily_path)

    # 计算每个级别对应的天数
    aqi_counts = daily_average['AQI'].value_counts().sort_index()
    aqi_counts.to_csv(counts_path)


if __name__ == "__main__":
    data_path = "./BeijingPM20100101_20151231.csv"
    process_humi_pres_temp(data_path, "./humi_pres_temp.csv")
    process_pm_data(data_path, "./pm.csv")
    process_cbwd_data(data_path, "./cbwd.csv")
    normalize_and_scatter(data_path, "./scatter.png")
    calculate_air_quality("./pm.csv", "./daily_pm.csv", "./counts.csv")
