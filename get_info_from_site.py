from bs4 import BeautifulSoup
import requests


def list_of_olimpiads(olimp, params):
    url = f'https://olimpiada.ru/activities'
    res = requests.get(url, params=params)
    soup = BeautifulSoup(res.text, 'html.parser')
    res = soup.find_all('div', class_='all')[2].find_all('div', class_='content')[0].find_all('div', id='megalist')[0]
    while res:
        url = f'https://olimpiada.ru/activities'
        res = requests.get(url, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')
        res = soup.find_all('div', class_='all')[2].find_all('div', class_='content')[0].find_all('div', id='megalist')[0]
        res = res.find_all('div', class_='fav_olimp olimpiada')

        for i in res:
            row = i.find('div', class_='o-block').find('div', class_='o-info').find('span', class_='headline')
            if olimp.lower() in row.get_text().lower():
                print(row.get_text())
        params['cnow'] = str(int(params['cnow']) + 20)
