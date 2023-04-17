import json

from get_info_from_site import list_of_olimpiads


def get_olimpiads(subject_name='', class_name='any', olimp=''):

    params = {
        'class': class_name,
        'type': 'any',
        'period': 'year',
        'period_date': '',
        'cnow': '0'
    }

    if subject_name:
        with open('subject_to_code.json', encoding='utf-8') as json_file:
            subject = json.load(json_file)[subject_name]
        params[f'subject[{subject}]'] = 'on'

    return list_of_olimpiads(olimp, params)

