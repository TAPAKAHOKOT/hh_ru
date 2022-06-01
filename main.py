import grequests
import requests as r

base_url = 'https://api.hh.ru'
get_vacancies_url = base_url + '/vacancies'


response_text = 'PHP'
print(f'response text=<{response_text}>')
def get_response_params(page: int = 0) -> dict:
	return {
		'text': response_text,
		'per_page': 100,
		'page': page,
		'only_with_salary': True
	}
def get_max_page() -> int:
	response = r.get(get_vacancies_url, params=get_response_params())
	data = response.json()

	return data['pages']

max_page = get_max_page()
items = []

def save_response_data(results: list):
	for result in results:
		data = result.json()
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

def send_response(start_page: int,  end_page: int):
	response = (grequests.get(get_vacancies_url, data=get_response_params(page)) for page in range(start_page, end_page))
	results = grequests.map(response)
	save_response_data(results)

def count_salary():
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
	print(f'middle salary=<{round(sr_from/items_count):_} - {round(sr_to/items_count):_}>')


step = 5
for k in range(0, max_page, step):
	send_response(k, k + step)
print(f'items founded=<{len(items)}>')
count_salary()
