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
            row = i.find('div', class_='o-block').find('div', class_='o-info').find('a', class_='none_a black').find('span', class_='headline')
            href = i.find('div', class_='o-block').find('div', class_='o-info').find('a', class_='none_a black')['href']
            subjects = i.find('div', class_='o-block').find('div', class_='o-tags').find('div', class_='subject_tags')
            classes = subjects.find('span', class_='classes_dop').get_text()
            min_class = 1
            max_class = 11
            if classes:
                classes = classes.split()[0]
                if len(classes.split('-')) < 2 and len(classes.split('–')) < 2 and ',' not in classes:
                    min_class = int(classes)
                    max_class = int(classes)
                elif ',' in classes:
                    min_class = int(classes.split(',')[0])
                    max_class = int(classes.split(',')[-1])
                elif len(classes.split('-')) < 2:
                    min_class = int(classes.split('–')[0])
                    max_class = int(classes.split('–')[1])
                else:
                    min_class = int(classes.split('-')[0])
                    max_class = int(classes.split('-')[1])
            subjects = subjects.find_all('span', class_='subject_tag')
            timeline = i.find('div', class_='timeline')
            red_dates = []
            super_light_blue_dates = []
            light_blue_dates = []
            blue_dates = []
            grey_dates = []
            grey_line = i.find('div', class_='o-block').find('div', class_='o-info')
            if grey_line.find('a', class_='none_a black olimp_desc'):
                grey_line = ''.join(grey_line.find('a', class_='none_a black olimp_desc').get_text().split('\xa0')).strip()
            else:
                grey_line = ''

            if timeline:
                red_dates = timeline.find_all('div', class_='tl_event enow')
                super_light_blue_dates = timeline.find_all('div', class_='tl_event long')
                light_blue_dates = timeline.find_all('div', class_='tl_event ereg')
                blue_dates = timeline.find_all('div', class_='tl_event eoch')
                grey_dates = timeline.find_all('div', class_='tl_event eold')
            if olimp.lower() in row.get_text().lower():
                lst.append((''.join(row.get_text().split('\xa0')).strip(),
                            [(' '.join(p.get_text().split('\xa0'))).strip() for p in subjects], grey_line, href,
                            red_dates, super_light_blue_dates, light_blue_dates, blue_dates, grey_dates, min_class,
                            max_class))

        params['cnow'] = str(int(params['cnow']) + 20)
    return lst