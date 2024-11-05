import requests
from bs4 import BeautifulSoup

url_1: str = "https://www.legislation.gov.uk/uksi/2008/944/schedule/1/made"
url_2: str = ""

response_1: requests.models.Response = requests.get(url_1)
print(response_1.status_code)
soup1: BeautifulSoup = BeautifulSoup(response_1.text, 'html.parser')
# print(soup1)
# soup1_p = soup1.p["LegP1ParaText"]
# print(len(soup1_p))"
soup1_content_div = soup1.find_all('div', id="viewLegSnippet")[0]
print(len(soup1_content_div))
soup1_content_paragraphs = soup1_content_div.find_all('p', class_="LegP1ParaText",)
# print(soup1_content_paragraphs)

url_1_pathogens: list[str] = []
for p in soup1_content_paragraphs:
    em_tag = p.find_all('em')
    if len(em_tag) != 0:
        url_1_pathogens.append(em_tag[0].get_text())
    else:
        temp = p.get_text()
        # print(temp)
        temp_processed = temp.split('.')[-1].strip()
        # print(temp_processed)
        url_1_pathogens.append(temp_processed)
    

print(url_1_pathogens)