import datetime

# dates
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
YESTERDAY = datetime.datetime.today()-datetime.timedelta(1)
YESTERDAY_CUT = YESTERDAY.strftime('%Y-%m-%d')

# plots
GRAPH_MIN_CASES = '100'