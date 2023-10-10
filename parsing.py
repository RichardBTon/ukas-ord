from bs4 import BeautifulSoup
from getHTML import getHTML
import json
import re

webpage = "https://naob.no/ordbok/ost"

soup = BeautifulSoup(getHTML(webpage), 'html.parser')
html = soup.find("div", {"class": "article"})

# To avoid running selenium every time for tests:
# with open("article.html", "r") as file:
#     html = file.read()
#################################################
with open("ost.html", "w") as file:
    file.write(str(html))

def get_definition(meaning) -> str:
    defintion = ''
    # Only add text from direct child divs of the 'betydning' div that have the 'inline-eske' class
    for def_div in meaning.find_all('div', class_='inline-eske', recursive=False):
        defintion += ' ' + def_div.text.strip()
    defintion = defintion.strip()
    return defintion


def get_meaning_quotes(meaning) -> dict:
    """Takes in meaning (soup) and meaningdata (dict) and appends quotes to meaningdata"""
    quotes = meaning.find('div', class_='sitatseksjon')
    quotes_data = []
    if quotes:            
         for quote in quotes.find_all('div', class_='sitat'):
                quotes_data.append(quote.text.strip())
    return quotes_data

def add_submeanings(parentmeaning, meaning_nr, meanings, i=0) -> int:
    if parentmeaning == None:
        parentmeaning = []

    meaning = meanings[i]
    meaning_data = {
            'meaningnr': meaning_nr,
            'definition': get_definition(meaning),
            'quotes': get_meaning_quotes(meaning),
            'submeanings': [],
        }

    parentmeaning["submeanings"].append(meaning_data)
    if re.search("\d.", meaning_nr):
        i += 1
        meaning_nr=meaning_nr[2:] # 1.2 -> 2
        add_submeanings(parentmeaning=meaning_data, meaning_nr=meaning_nr, meanings=meanings, i=i) 
    return i
    
def parse_article_html(soup) -> dict:
    
    data = {
        'word': soup.find('span', class_='oppslagsord').text.strip(),
        'type': soup.find('div', class_='ordklasseledd').text.strip(),
        'etymology': soup.find('div', class_='inline-eske').text.strip(),
        'meanings': [],
    }
    
    meanings = soup.find_all('div', class_='betydning')
    meaning_nrs = soup.find_all("span", class_="betydningnr") #Fordrer at betydningsnr kommer i samme rekkefølge som betydning

    for i, meaning in enumerate(meanings):

        meaning_nr = meaning_nrs[i]
        # Adding the definition
        meaning_data['definition'] = get_definition(meaning)
        
        # Adding the quotes
        meaning_data['quotes'] = get_meaning_quotes(meaning)
        

        data['meanings'].append(meaning_data)

        
    return data


# Test
# html = """ ... your provided HTML here ... """
result = parse_article_html(html)
print(json.dumps(result, indent=4))
