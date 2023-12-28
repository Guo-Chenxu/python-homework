import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def scatter(csv_path: str, scatter_path: str):
    """
    散点图
    """
    df = pd.read_csv(csv_path)

    price_per_unit = df['均价']
    total_price = df['总价']
    property_type = df['类型']

    unique_types = property_type.unique()

    num_colors = len(unique_types)
    colors = plt.cm.tab10.colors[:num_colors]
    color_map = dict(zip(unique_types, colors))
    colors = [color_map.get(prop_type, 'gray') for prop_type in property_type]

    plt.figure()
    plt.title('房价与总价散点图')
    plt.xlabel('单价/(万元/㎡)')
    plt.ylabel('总价/万元')
    plt.scatter(price_per_unit, total_price, c=colors, s=10)

    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=prop_type, markerfacecolor=color)
                       for prop_type, color in color_map.items()]
    plt.legend(handles=legend_elements, title='类型', loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.savefig(scatter_path, bbox_inches='tight')
    plt.close()


def avg_bar(csv_path: str, avg_bar_path: str):
    """
    绘制均价的直方图
    """
    data = pd.read_csv(csv_path)

    grouped_data = data.groupby('行政区').agg({'均价': 'mean', '楼盘名称': 'size'})
    grouped_data = grouped_data.rename(columns={'均价': '平均单价'})
    grouped_data = grouped_data.rename(columns={'楼盘名称': '楼盘数量'})

    plt.figure()
    plt.bar(grouped_data['楼盘数量'], grouped_data['平均单价'])
    plt.xticks(grouped_data['楼盘数量'])
    plt.yticks(np.arange(0, max(grouped_data['平均单价']) + 3, 3))

    plt.xlabel('楼盘数量/个')
    plt.ylabel('平均单价/(万元/㎡)')
    plt.title('各行政区平均单价和楼盘数量直方图')

    # 在每个柱子上方标注行政区名称
    for i, district in enumerate(grouped_data.index):
        names = district.split('/')
        names_str = ' / '.join(names)
        plt.text(grouped_data['楼盘数量'].iloc[i], grouped_data['平均单价'].iloc[i], names_str, ha='center')

    plt.savefig(avg_bar_path, bbox_inches='tight')


def tot_bar(csv_path='./new_house.csv', tot_bar_path='./tot_bar.png'):
    """
    绘制平均总价的直方图
    """
    data = pd.read_csv(csv_path)

    grouped_data = data.groupby('行政区').agg({'总价': 'mean', '楼盘名称': 'size'})
    grouped_data = grouped_data.rename(columns={'总价': '平均总价'})
    grouped_data = grouped_data.rename(columns={'楼盘名称': '楼盘数量'})

    plt.figure()
    plt.bar(grouped_data['楼盘数量'], grouped_data['平均总价'])
    plt.xticks(grouped_data['楼盘数量'])
    plt.yticks(np.arange(0, max(grouped_data['平均总价']) + 200, 200))

    plt.xlabel('楼盘数量/个')
    plt.ylabel('平均总价/万元')
    plt.title('各行政区平均总价和楼盘数量直方图')

    # 在每个柱子上方标注行政区名称
    for i, district in enumerate(grouped_data.index):
        names = district.split('/')
        names_str = ' / '.join(names)
        plt.text(grouped_data['楼盘数量'].iloc[i], grouped_data['平均总价'].iloc[i], names_str, ha='center')

    plt.savefig(tot_bar_path, bbox_inches='tight')


def pie(csv_path: str, pie_path: str):
    """
    绘制饼图
    """
    data = pd.read_csv(csv_path)

    data['均价分布'] = pd.cut(data['均价'], [0, 5, 10, 15, 20])
    count_by_plate = data['均价分布'].value_counts()

    plt.figure()
    plt.pie(count_by_plate, labels=count_by_plate.index, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('北京新房均价分布(万元/㎡)')

    plt.savefig(pie_path, bbox_inches='tight')


if __name__ == '__main__':
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    scatter(csv_path='./new_house.csv', scatter_path='./scatter.png')
    avg_bar(csv_path='./new_house.csv', avg_bar_path='./avg_bar.png')
    tot_bar(csv_path='./new_house.csv', tot_bar_path='./tot_bar.png')
    pie(csv_path='./new_house.csv', pie_path='./pie.png')
