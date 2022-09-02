import requests
from bs4 import BeautifulSoup
import pandas as pd


# I pull tables with a GAME url
def pull_tables(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    data = []
    for table in soup.find_all('table')[1:4]:
        data.append(
            pd.read_html(table.prettify())
        )
    output = {
        'MatchData': {
            'HomeTeam': data[0][0].iloc[1,1].replace('»', '').strip(),
            'HomeScore': int(data[0][0].iloc[1,2].strip()),
            'AwayTeam': data[0][0].iloc[1,4].replace('»', '').strip(),
            'AwayScore': int(data[0][0].iloc[1,5].strip()),
            'Ground': data[0][0].iloc[1,6].strip('- '),
            'Datetime': data[0][0].iloc[1,7].strip()
        },
        'Home': {
            'Lineup': data[1][0].iloc[:-2,],
            'PenaltyTries': int(data[1][0].iloc[-2, 3])
        },
        'Away': {
            'Lineup': data[2][0].iloc[:-2, ],
            'PenaltyTries': int(data[2][0].iloc[-2, 3])
        }
    }
    output['Home']['Lineup'].columns = output['Home']['Lineup'].iloc[0]
    output['Home']['Lineup'] = output['Home']['Lineup'].drop(output['Home']['Lineup'].index[0])
    output['Away']['Lineup'].columns = output['Away']['Lineup'].iloc[0]
    output['Away']['Lineup'] = output['Away']['Lineup'].drop(output['Away']['Lineup'].index[0])
    return output


# I scrape through the main website to get href tags
def href_scraper():
    base_url = 'https://rugbyresults.fusesport.com/competitions.asp'
    # I want to select the top 'Schedule and Standings' so that it works once the next season starts
    soup = BeautifulSoup(requests.get(base_url).text, 'html.parser')
    names = [i.text.replace('\r', '').replace('\t', '').replace('\n', '') for i in soup.find_all('div', class_='competitions')[0].find_all('a')]
    links = [i['href'] for i in soup.find_all('div', class_='competitions')[0].find_all('a')]
    div_list = []
    i = 0
    while i < len(names):
        div_list.append(
            {
                'Div_name': names[i],
                'Link': links[i]
            }
        )
        i += 1
    cup_list = []
    for elem in div_list:
        soup = BeautifulSoup(requests.get('https://rugbyresults.fusesport.com/competitions.asp' + elem['Link']).text, 'html.parser')
        names = [i.text for i in soup.find_all('table')[0].find_all('td', attrs={'colspan': '2'})]
        links = [i.find('a')['href'] for i in soup.find_all('table')[0].find_all('td', attrs={'class': 'schedule'})]
        i = 0
        while i < len(names):
            cup_list.append(
                {
                    'Div_name': elem['Div_name'],
                    'Cup_name': names[i],
                    'Link': links[i]
                }
            )
            i += 1
    for cup in cup_list:

