import requests
endpoint = 'https://www.balldontlie.io/api/v1/players?per_page=5'

# Get All Players
# r = requests.get('https://www.balldontlie.io/api/v1/players?per_page=5')
# print(r.json())
# print(r.status_code)

# Player Search with params
query = {'search': 'durant'}
r = requests.get(endpoint, params=query)
print(r.url)
print(r.json())
print(r.status_code == requests.codes.ok)

# Get Player Search with input
# query = input('Search by player name: ')
# r = requests.get(f"{endpoint}&search={query}")
# print(r.url)
# print(r.json())
# print(r.status_code)
# print(r.status_code == requests.codes.ok)
# data = r.json()['data']
# print(data[0]['first_name'])
# print(r.json()['data']['first_name'])
# print(r.text)