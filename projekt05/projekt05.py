import requests
from bs4 import BeautifulSoup
import json
import argparse

url = 'https://krainaserow.pl/catalog?filter_all_categories=15'

parser = argparse.ArgumentParser()
parser.add_argument('save_path', type=str, help='ścieżka do pliku z nazwami serów')
args = parser.parse_args()

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
main_div = soup.find('div', class_='row mt-3')

cheese_names = []
for cheese in main_div.find_all('h5'):
    cheese_names.append(cheese.text)

with open(args.save_path, 'w') as file:
    json.dump(cheese_names, file)

#python projekt05/projekt05.py projekt05/cheese_names.json