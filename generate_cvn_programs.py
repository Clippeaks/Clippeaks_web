import json
import os
import csv
from datetime import datetime

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_current_day():
    return datetime.now().weekday() + 1  # Monday is 0, Sunday is 6

def filter_data(data, region, end_time):
    filtered_data = [item for item in data if item['Region'] == region and datetime.strptime(item['Timestamp'], '%Y-%m-%d %H:%M:%S') < end_time]
    return sorted(filtered_data, key=lambda x: float(x['Estimated_Total_SC']), reverse=True)[:10]

def fetch_exchange_rates():
    try:
        import requests
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch exchange rates")
    except:
        try:
            with open('/Volumes/KIOXIA/clippeaks/rates_cache.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("No cache found. Please provide a valid API key or use the local cache.")
            exit(1)

def convert_currency(data, base_currency):
    exchange_rates = fetch_exchange_rates()
    conversion_factor = exchange_rates['rates'][base_currency]
    for item in data:
        item['Currency_Normalized_JPY'] = float(item['SC_Currency']) * conversion_factor
    return data

def main():
    master_data_path = '/Volumes/KIOXIA/clippeaks/master.csv'
    output_path = '/Volumes/KIOXIA/clippeaks/output/special_program.json'

    # Read master data
    master_data = read_csv(master_data_path)

    current_day = get_current_day()
    end_time = datetime.now()  # Placeholder for actual end time

    if current_day == 1:  # Monday - EN Week Recap & Whale Watcher
        filtered_data = filter_data(master_data, 'EN', end_time)
    elif current_day == 2:  # Tuesday - JAPAN Week Recap & Hidden Gem
        filtered_data = filter_data(master_data, 'JP', end_time)
    elif current_day == 3:  # Wednesday - ID Week Recap & Risk Analysis
        filtered_data = filter_data(master_data, 'ID', end_time)
    elif current_day == 4:  # Thursday - The Global Whale Ranking / 一撃クジラ王
        filtered_data = master_data
        filtered_data = convert_currency(filtered_data, 'USD')
        filtered_data = convert_currency(filtered_data, 'JPY')

    output = {}
    for i, item in enumerate(filtered_data, start=1):
        output[f"Rank_{i}"] = {
            "Metadata": {
                "VTuber": item['Name'],
                "Region": item['Region'],
                "Topic_Type": item['Category']
            },
            "Data_Points": {
                "PeakScore": float(item['Estimated_Total_SC']),
                "Density": float(item['Engagement_Density']),
                "Max_SC_JPY": int(item['Currency_Normalized_JPY']),
                "Max_SC_USD": int(float(item['SC_Currency']) * exchange_rates['rates']['USD'])
            },
            "Script_Assets": {
                "Headline": f"【自動生成】{item['Title']}",
                "Narrative": [
                    item['Context_1'],
                    item['Context_2'],
                    item['Context_3']
                ],
                "Punchline": item['Punchline']
            }
        }

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(output, file, indent=4)

if __name__ == '__main__':
    main()