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
