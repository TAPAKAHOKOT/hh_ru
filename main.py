import requests as r

base_url = 'https://api.hh.ru'
get_vacancies_url = base_url + '/vacancies'

response_params = {
	'text': 'PHP',
	'per_page': 100,
	'page': 0
}

response_data = {}
max_page = None
is_first_response = True
while True:
	response = r.get(get_vacancies_url, params=response_params)
	data = response.json()

	if is_first_response:
		is_first_response = False
		max_page = data['pages']

	items = []
	for item in data['items']:
		if item['salary'] is None:
			continue
		items.append({
			'name': item['name'],
			'salary': {
				'from': item['salary']['from'],
				'to': item['salary']['to']
			}
		})

	response_data[response_params['page']] = data

	response_params['page'] += 1
	print(response_params['page'], '/', max_page)
	if response_params['page'] >= max_page:
		break

print(len(response_data))

sr_from = 0
sr_to = 0
for item in items:
	if item['salary']['from'] is not None:
		sr_from += item['salary']['from']

	if item['salary']['to'] is not None:
		sr_to += item['salary']['to']

	if item['salary']['from'] is not None and item['salary']['to'] is None:
		sr_to += item['salary']['from']

items_count = len(items)
print(f'{round(sr_from/items_count):_} - {round(sr_to/items_count):_}')
