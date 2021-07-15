import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

BASE_URLS = {
    'ppr': 'https://www.fantasypros.com/nfl/adp/ppr-overall.php',
    'half_ppr': 'https://www.fantasypros.com/nfl/adp/half-point-ppr-overall.php',
    'standard': 'https://www.fantasypros.com/nfl/adp/overall.php'
}

for league_format, BASE_URL in BASE_URLS.items():
  res = requests.get(BASE_URL)
  if res.ok:
    soup = BS(res.content, 'html.parser') # grabbing the HTML content of the response
    table = soup.find('table', {'id': 'data'}) # finding the specific table by ID
    df = pd.read_html(str(table))[0] # setting the data frame to the specific table

    df = df.iloc[:, 1:] # removing the first column on our dataframe. It's an unneccessary index column
    df = df[['Player Team (Bye)', 'POS', 'AVG']] # choosing columns for data frame
    df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2])) # removing the team and position from Player column
    df['POS'] = df['POS'].apply(lambda x: x[:2]) # removing the position rank

    df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
    df.to_csv(f'fantasypros/data/adp/{league_format}_adp.csv')

    print(f'Scrape successful: /fantasypros/data/adp/{league_format}_adp.csv')
  else:
    print('Sorry, something didn\'t work right', res.status_code)
    break
