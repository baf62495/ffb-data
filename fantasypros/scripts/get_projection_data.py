import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from utils import rename_dupe_col

# TODO: Do other league formats also

BASE_URL = 'https://www.fantasypros.com/nfl/projections/{pos}.php?week=draft&scoring=HALF'

positions = [
  'te',
  'wr',
  'qb',
  'rb',
]

dfs = []

for pos in positions:
  res = requests.get(BASE_URL.format(pos = pos))
  if res.ok:
    soup = BS(res.content, 'html.parser') # grabbing the HTML content of the response
    table = soup.find('table', {'id': 'data'}) # finding the specific table by ID
    df = pd.read_html(str(table))[0] # setting the data frame to the specific table

    df.columns = df.columns.droplevel(level = 0)
    df['Pos'] = pos.upper()
    
    df['Team'] = df['Player'].apply(
      lambda x: x.split()[-1]
    ) # taking team abbreviation from player name and creating a team column
    df['Player'] = df['Player'].apply(
      lambda x: ' '.join(x.split()[:-1])
    ) # removing team abbreviation from player name

    if pos == 'rb':
      df = df.rename({
        'ATT': 'Rush Att',
        'REC': 'Rec',
        'FL': 'Fum',
        'FPTS': 'Fantasy Points',
      }, axis = 1)

      rename_dupe_col(df, 'Rush Yds', 'YDS', 0)
      rename_dupe_col(df, 'Rec Yds', 'YDS', 1)
      rename_dupe_col(df, 'Rush TDs', 'TDS', 0)
      rename_dupe_col(df, 'Rec TDs', 'TDS', 1)

      df = df.drop([
        'YDS',
        'TDS'
      ], axis = 1)

      ordered_cols = [
        'Player',
        'Team',
        'Pos',
        'Rush Att',
        'Rush Yds',
        'Rush TDs',
        'Rec',
        'Rec Yds',
        'Rec TDs',
        'Fum',
        'Fantasy Points'
      ]

      df = df[ordered_cols].sort_values(by = 'Fantasy Points', ascending = False)
      

    if pos == 'wr':
      df = df.rename({
        'ATT': 'Rush Att',
        'REC': 'Rec',
        'FL': 'Fum',
        'FPTS': 'Fantasy Points',
      }, axis = 1)

      rename_dupe_col(df, 'Rush Yds', 'YDS', 1)
      rename_dupe_col(df, 'Rec Yds', 'YDS', 0)
      rename_dupe_col(df, 'Rush TDs', 'TDS', 1)
      rename_dupe_col(df, 'Rec TDs', 'TDS', 0)

      df = df.drop([
        'YDS',
        'TDS'
      ], axis = 1)

      ordered_cols = [
        'Player',
        'Team',
        'Pos',
        'Rec',
        'Rec Yds',
        'Rec TDs',
        'Rush Att',
        'Rush Yds',
        'Rush TDs',
        'Fum',
        'Fantasy Points'
      ]

      df = df[ordered_cols].sort_values(by = 'Fantasy Points', ascending = False)

    if pos == 'qb':
      df =df.rename({
        'CMP': 'Pass Comp',
        'INTS': 'Ints',
        'FL': 'Fum',
        'FPTS': 'Fantasy Points',
      }, axis = 1)

      rename_dupe_col(df, 'Pass Yds', 'YDS', 0)
      rename_dupe_col(df, 'Rush Yds', 'YDS', 1)
      rename_dupe_col(df, 'Pass TDs', 'TDS', 0)
      rename_dupe_col(df, 'Rush TDs', 'TDS', 1)
      rename_dupe_col(df, 'Pass Att', 'ATT', 0)
      rename_dupe_col(df, 'Rush Att', 'ATT', 1)

      df = df.drop([
        'YDS', 'TDS', 'ATT'
      ], axis=1)

      ordered_cols = [
        'Player',
        'Team',
        'Pos',
        'Pass Att',
        'Pass Comp',
        'Pass Yds',
        'Pass TDs',
        'Ints',
        'Rush Att',
        'Rush Yds',
        'Rush TDs',
        'Fum',
        'Fantasy Points'
      ]

      df = df[ordered_cols].sort_values(by = 'Fantasy Points', ascending = False)

    if pos == 'te':
      df = df.rename({
        'REC': 'Rec',
        'YDS': 'Rec Yds',
        'TDS': 'Rec TDs',
        'FL': 'Fum',
        'FPTS': 'Fantasy Points'
      }, axis = 1)

      ordered_cols = [
        'Player',
        'Team',
        'Pos',
        'Rec',
        'Rec Yds',
        'Rec TDs',
        'Fum',
        'Fantasy Points'
      ]

      df = df[ordered_cols].sort_values(by = 'Fantasy Points', ascending = False)

    df.to_csv(f'fantasypros/data/projections/half_ppr/{pos}.csv')
    print(f'Scrape successful: fantasypros/data/projections/half_ppr/{pos}.csv')
    
    dfs.append(df)


  else:
    print('Sorry, something didn\'t work right', res.status_code)
    break

  df = pd.concat(dfs).fillna(0)
  columns = [column for column in df.columns if column != 'Fantasy Points'] + ['Fantasy Points'] # moving fantasy points column to last column in data frame
  df = df[columns]
  df = df.sort_values(by = 'Fantasy Points', ascending = False)

df.to_csv('fantasypros/data/projections/half_ppr/all.csv')
print('Scrape successful: /fantasypros/data/projections/half_ppr/all.csv')