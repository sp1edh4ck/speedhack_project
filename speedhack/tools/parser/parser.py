import requests
from bs4 import BeautifulSoup as BS

username = 'sp1edh4ck'

r = requests.get(f"https://steamcommunity.com/id/{username}")
html = BS(r.content, 'html.parser')

for el in html.select(".profile_header_centered_persona"):
    title = el.select(".persona_name > span")
    print(title[0].text)
