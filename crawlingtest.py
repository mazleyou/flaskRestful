from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://dictionary.cambridge.org/ko/%EC%82%AC%EC%A0%84/%EC%98%81%EC%96%B4/' + 'photon')
bsObject = BeautifulSoup(html, 'html.parser')


my_titles = bsObject.select(
    'span.us.dpron-i > span.pron.dpron > span'
    )
print(my_titles[0].text)

