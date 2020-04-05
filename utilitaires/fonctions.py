import os
import csv
from datetime import datetime


TODAY = datetime.today().strftime('%Y-%m-%d')

def clean_folder():
	try:
		os.remove('full_data.csv')
	except:
		pass

	try:
		os.system('rm -r out/')
	except:
		pass


def get_list_countries(data):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		list_countries = []
		for line in f_o:
			if line[1] not in list_countries:
				list_countries.append(line[1])
		return list_countries


def get_all_dates(data):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		list_all_dates = []
		for line in f_o:
			if line[0] not in list_all_dates:
				list_all_dates.append(line[0])
		return list_all_dates


def get_data_today(data):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		dictionnary_data_today = {}
		for line in f_o:
			if line[0] == TODAY:
				data = [line[2], line[3], line[4], line[5]]
				dictionnary_data_today[line[1]] = data
		return dictionnary_data_today