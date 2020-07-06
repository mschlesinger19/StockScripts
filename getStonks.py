import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.gurufocus.com/stock_list.php?m_country[]=USA&p=0&n=100")
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.findAll('a')
stonks = []
for link in links:
    if "LAST (" in link.text:
        lastPage = link.text.split('(')[1].lstrip().split(')')[0]
        break;
for i in range (0, int(lastPage)):
    html = "https://www.gurufocus.com/stock_list.php?m_country[]=USA&p=" + str(i) + "&n=100"
    page = requests.get(html)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', id="R1")
    rows = table.findAll('tr')
    for row in rows:
        links = row.findAll('a')
        if (links):
            link = links[0]
            if (link.text != 'Symbol'):
                print(link.text)