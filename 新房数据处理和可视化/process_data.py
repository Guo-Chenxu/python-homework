import csv
import json
import re

if __name__ == '__main__':
    with open('new_house.json', 'r', encoding='utf-8') as json_file, open('new_house.csv', 'w',
                                                                          encoding='utf-8', newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        header = ['楼盘名称', '类型', '行政区', '乡镇区域', '街道', '房型', '面积', '总价', '均价']
        csv_writer.writerow(header)

        for line in json_file:
            json_data = json.loads(line)

            house_type = json_data['type'].strip() if not str(json_data['type'].strip()).endswith('类') \
                else str(json_data['type'].strip())[:-1]
            location = json_data['location'].split('/')
            area = re.search(r'\d+', str(json_data.get('area', '0')))
            min_area = int(area.group()) if area else 0
            unit_price = round(int("".join(filter(str.isdigit, json_data['unit_price']))) / 10000)

            row = [
                json_data['name'].strip(),
                house_type,
                location[0].strip(),
                location[1].strip(),
                location[2].strip(),
                json_data['room_type'].split('/')[0].strip(),
                min_area,
                min_area * unit_price,
                unit_price
            ]
            csv_writer.writerow(row)
