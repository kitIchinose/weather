from datetime import datetime
import requests

from line_notify import line_notify

SHIZUOKA_CODE = 220000


def get_weather(code):
    # 3日間(最大)の天気予報を取得
    api_url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json'
    # weather_data = requests.get(api_url)  # サーバへのリクエスト
    # print(weather_data)
    weather_data = requests.get(api_url).json()  # json形式でデータを受け取る
    # print(weather_data) # listで受け取る

    area_name = weather_data[0]['publishingOffice'][:-5] + weather_data[0]['timeSeries'][0]['areas'][2]['area']['name']
    # print(area_name)
    time_series = weather_data[0]['timeSeries'][0]['timeDefines']
    # print(time_series)
    weather_series = weather_data[0]['timeSeries'][0]['areas'][2]['weathers']
    # print(weather_series)

    weathers = f'{len(time_series)}日間の天気予報\n'
    for time, weather in zip(time_series, weather_series):
        # print(type(time), f'{time}の{area_name}の天気は{weather}です。')
        time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')  # 文字列をdate型に変換する関数
        # print(type(time), f'{time}の{area_name}の天気は{weather}です。')
        weathers += f'\t{time}の {area_name}の天気は {weather}です。\n'
    else:
        weathers += '\n'
    # print(weathers)

    # 天気予報の詳細を取得
    detail_url = f'https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{code}.json'
    weather_data = requests.get(detail_url).json()  # json形式でデータを受け取る
    weathers += weather_data['text']
    # print(weathers)
    return weathers


weather_info = get_weather(SHIZUOKA_CODE)
print(weather_info)
line_notify(weather_info)
