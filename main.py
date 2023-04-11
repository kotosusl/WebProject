import json

from get_info_from_site import list_of_olimpiads

subject_name = 'биология'
class_name = 'any'
olimp = ''

with open('subject_to_code.json', encoding='utf-8') as json_file:
    subject = json.load(json_file)[subject_name]

params = {
    f'subject[{subject}]': 'on',
    'class': class_name,
    'type': 'any',
    'period': 'year',
    'period_date': '',
    'cnow': '0'
}
print(params)
print(list_of_olimpiads(olimp, params))

