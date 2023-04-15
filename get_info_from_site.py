from bs4 import BeautifulSoup
import requests


def list_of_olimpiads(olimp, params):
    url = f'https://olimpiada.ru/activities'
    res = requests.get(url, params=params)
    soup = BeautifulSoup(res.text, 'html.parser')
    res = soup.find_all('div', class_='all')[2].find_all('div', class_='content')[0].find_all('div', id='megalist')[0]
    lst = []
    while res:
        url = f'https://olimpiada.ru/activities'
        res = requests.get(url, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')
        res = soup.find_all('div', class_='all')[2].find_all('div', class_='content')[0].find_all('div', id='megalist')[0]
        res = res.find_all('div', class_='fav_olimp olimpiada')

        for i in res:
            row = i.find('div', class_='o-block').find('div', class_='o-info').find('span', class_='headline')
            subjects = i.find('div', class_='o-block').find('div', class_='o-tags').find('div', class_='subject_tags')
            subjects = subjects.find_all('span', class_='subject_tag')
            if olimp.lower() in row.get_text().lower():
                lst.append((''.join(row.get_text().split('\xa0')).strip(), [(' '.join(p.get_text().split('\xa0'))).strip() for p in subjects]))
        params['cnow'] = str(int(params['cnow']) + 20)
    return lst