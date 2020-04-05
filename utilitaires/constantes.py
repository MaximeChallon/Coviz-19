import datetime

# dates
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
YESTERDAY = datetime.datetime.today()-datetime.timedelta(1)
YESTERDAY_CUT = YESTERDAY.strftime('%Y-%m-%d')

# plots
GRAPH_MIN_CASES = '100'
DEFAULT = (16,7)
LESS_15D = (8,5)
MORE_30D = (20, 12)
COLOR = 'r'
GRAPH_MIN_TOTAL_DECEASES = 5