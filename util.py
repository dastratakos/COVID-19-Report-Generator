import json

import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

FILENAMES = {
    True: {                                                 # US
        True: 'time_series_covid19_confirmed_US.csv',           # CASES
        False: 'time_series_covid19_deaths_US.csv',             # DEATHS
    },
    False: {                                                # GLOBAL
        True: 'time_series_covid19_confirmed_global.csv',       # CASES
        False: 'time_series_covid19_deaths_global.csv',         # DEATHS
    }
}

with open('./abbreviations.json') as f:
    STATE_TO_ABBREV = json.load(f)
ABBREV_TO_STATE = dict(map(reversed, STATE_TO_ABBREV.items()))

START_DATE      = '1/22/20'
TEST_DATE       = '10/20/20'
TEST_STATES     = ['California', 'New York', 'Florida']
TEST_COUNTRIES  = ['India', 'US', 'Brazil']

def loadData(US=True, cases=True, use_local=False):
    try:
        PATH = DATA_URL + FILENAMES[US][cases]
        return pd.read_csv(PATH)
    except URLError(err):
        PATH = './data/' + FILENAMES[US][cases]
        return pd.read_csv(PATH)

def test(title, test):
    print(f'===== {title} =====')
    try: assert test; print('PASSED')
    except: print('***** FAILED *****')

if __name__ == '__main__':
    test('Test 1: California --> CA?', STATE_TO_ABBREV['California'] == 'CA')
    test('Test 2: CA --> California?', ABBREV_TO_STATE['CA'] == 'California')
    test('Test 3: 56 total entries? (50 states, DC, 5 territories)', len(STATE_TO_ABBREV) == 56)

