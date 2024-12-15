import requests
import json
import csv

API_TOKEN = '6842c73159f51d5a07355cd16c09e76e'
POPULAR_ROUTES_API_URL = 'http://api.travelpayouts.com/v1/city-directions'
MONTH_MATRIX_API_URL = 'http://api.travelpayouts.com/v2/prices/month-matrix'

# Список аэропортов
popular_origin_cities = [
    'ABA', 'DYR', 'AAQ', 'ARH', 'ASF', 'BAX', 'EGO', 'BQS', 'BTK', 'BZK', 'VRI', 'VVO', 'OGZ', 'VOG', 'VOZ', 'GRV', 'SVX', 'ZIA', 'IKT', 
'KZN', 'KGD', 'KLF', 'KEJ', 'KRR', 'KJA', 'KRO', 'URS', 'LPK', 'IGT', 'GDX', 'MQF', 'MCX', 'MRV', 'VKO', 'DME', 'SVO', 'MMK', 'NAL', 
'NJC', 'NBC', 'GOJ', 'NOZ', 'OVB', 'NSK', 'OMS', 'REN', 'OSW', 'OSF', 'PEE', 'PES', 'PKC', 'PVS', 'PKV', 'ROV', 'SBT', 'KUF', 'LED', 
'SKX', 'GSV', 'SIP', 'AER', 'STW', 'SGC', 'SCW', 'RMZ', 'TOF', 'TJM', 'UUD', 'ULV', 'ULY', 'UFA', 'KHV', 'HMA', 'CSY', 'CEK', 'CEE', 
'HTA', 'ESL', 'UUS', 'YKS', 'IAR', 'VGD', 'RGK', 'IWA', 'JOK', 'KVX', 'KMW', 'KYZ', 'NNM', 'PEZ', 'SLY'
]
currency = 'rub'

# Общий список данных
all_city_data = []

for origin_city in popular_origin_cities:
    print(f"Обработка данных для города {origin_city}...")
    
    # 1. Получение популярных направлений
    print("  Получение популярных направлений...")
    popular_routes_payload = {
        'origin': origin_city,
        'currency': currency,
        'token': API_TOKEN
    }

    response = requests.get(POPULAR_ROUTES_API_URL, params=popular_routes_payload)
    if response.status_code != 200:
        print(f"  Ошибка при запросе популярных маршрутов для {origin_city}: {response.status_code} {response.text}")
        continue

    # Извлекаем данные маршрутов
    popular_routes = response.json().get('data', {}).keys()
    if not popular_routes:
        print(f"  Нет популярных маршрутов для города {origin_city}.")
        continue

    print(f"  Популярные направления из {origin_city}: {', '.join(popular_routes)}")

    # 2. Сбор данных за год для каждого направления
    city_data = []
    for destination in popular_routes:
        print(f"    Сбор данных за 2025 год для направления {destination}...")
        for month in range(1, 13):
            month_str = f"2025-{month:02d}-01"
            month_payload = {
                'origin': origin_city,
                'destination': destination,
                'currency': currency,
                'month': month_str,
                'token': API_TOKEN
            }
            # Выполняем запрос
            response = requests.get(MONTH_MATRIX_API_URL, params=month_payload)
            if response.status_code == 200:
                data = response.json().get('data', [])
                city_data.extend(data)
                print(f"      Месяц {month_str}: {len(data)} записей.")
            else:
                print(f"      Ошибка при запросе {month_str}: {response.status_code} {response.text}")

    # Добавляем данные города в общий список
    all_city_data.extend(city_data)

    # Сохраняем данные для текущего города в файл
    city_output_file = f"{origin_city}_routes_2025.csv"
    if city_data:
        with open(city_output_file, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = city_data[0].keys()  # Предполагаем, что все записи имеют одинаковые ключи
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Записываем заголовок
            writer.writeheader()
            
            # Записываем строки
            writer.writerows(city_data)
        
        print(f"  Данные для {origin_city} успешно записаны в {city_output_file}.")
    else:
        print(f"  Нет данных для записи для {origin_city}.")

# Сохраняем объединенные данные для всех городов
print("Сохранение общих данных...")

# Сохраняем в JSON
with open('all_cities_routes_2025.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_city_data, json_file, ensure_ascii=False, indent=4)

# Сохраняем в CSV
if all_city_data:
    output_file = "all_cities_routes_2025.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = all_city_data[0].keys()  # Предполагаем, что все записи имеют одинаковые ключи
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Записываем заголовок
        writer.writeheader()
        
        # Записываем строки
        writer.writerows(all_city_data)
    
    print(f"Общие данные успешно записаны в {output_file}.")
else:
    print("Нет данных для записи.")

print(f"Всего записей собрано: {len(all_city_data)}")
