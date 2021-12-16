import requests
import tweetDAO as dao

response = requests.get('https://httpbin.org/ip')

print('Your IP is {0}'.format(response.json()['origin']))

dao.initDB()