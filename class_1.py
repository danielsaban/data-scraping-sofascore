import requests
from bs4 import BeautifulSoup


r = requests.get('https://www.sofascore.com/it/squadra/calcio/inter/2697')

# r_2 = requests.get
# print(r)
# print(r.text)
#
# print(r.headers)
#
# print(r.encoding)

soup = BeautifulSoup(r, 'html.parser')
print(soup.prettify())

# list(soup.children)
#
# print(r.status_code)
#
# html = list(soup.children)[2]
# print(html)
#
# print([type(item) for item in list(soup.children)])
#
#
# body = list(html.children)[3]
#
#
# p = list(body.children)[1]
# p.get_text()
