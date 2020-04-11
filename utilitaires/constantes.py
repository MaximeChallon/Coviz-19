import datetime

# données
DATA = 'wget https://covid.ourworldindata.org/data/ecdc/full_data.csv'
DATA_BEGINNING = 'full_data.csv'
DATA_PATH = 'utilitaires/data/data_full.csv'

# dates
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
YESTERDAY = datetime.datetime.today()-datetime.timedelta(1)
YESTERDAY_CUT = YESTERDAY.strftime('%Y-%m-%d')

# plots
PLOT_MIN_CASES = '100'
DEFAULT = (16,7)
LESS_15D = (8,5)
MORE_30D = (25, 15)
COLOR = 'r'
PLOT_MIN_TOTAL_DECEASES = 5