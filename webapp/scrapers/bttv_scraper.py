import requests
from bs4 import BeautifulSoup as bs
import traceback
import urllib

BASE_QUERY = 'best time to visit'
BASE_URL = "https://www.google.co.in/search"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def get_html_page(place_name):
    url_query = "{} {}".format(BASE_QUERY, place_name)
    url = "{}?q={}".format(BASE_URL, url_query)
    response = requests.get(url, headers=headers, timeout=5)

    return response.content, response.status_code

def get_time_to_visit(place_name):

	response = {}

	html, status_code = get_html_page(place_name)
	if status_code != 200:
		response['status'] = 'NOT_FOUND'
		return response

	soup = bs(html, 'html.parser')
	try:
		data = soup.find_all('div', {'class': 'mod', 'data-md': '61'})[0]
		if data:
			response['status'] = 'FOUND'
			response['data'] = data.get_text()
		else:
			response['status'] = 'NOT_FOUND'
	except:
		response['status'] = 'NOT_FOUND'
		
	return response
