import os
import csv
from .constantes import *
import datetime

DATA_PATH = "full_data.csv"

def clean_folder():
	try:
		os.remove('full_data.csv')
	except:
		pass

	try:
		os.system('rm -r out/')
	except:
		pass


def get_list_countries_available(data):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		list_countries = []
		for line in f_o:
			if line[1] not in list_countries:
				list_countries.append(line[1])
		return list_countries


def get_all_dates_available(data):
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
				dictionnary_data_today[line[1]] = [line[2], line[3], line[4], line[5]]
	if len(dictionnary_data_today) == 0:
		with open(data, 'r') as f:
			f_o = csv.reader(f)
			next(f_o)
			dictionnary_data_today = {}
			for line in f_o:
				if line[0] == YESTERDAY_CUT:
					data = [line[2], line[3], line[4], line[5]]
					dictionnary_data_today[line[1]] = data
		print("Only yesterday's data are available now.")
		return dictionnary_data_today
	else:
		return dictionnary_data_today


def get_list_countries_to_process(country, full, liste):
	# list of countries to process
	list_countries_to_process = []
	if country in get_list_countries_available(DATA_PATH):
		list_countries_to_process.append(country)
	elif full:
		list_countries_to_process = get_list_countries_available(DATA_PATH)
	elif liste :
		liste = liste[1:-1]
		countries = liste.split(',')
		for one_country in countries:
			if one_country in get_list_countries_available(DATA_PATH):
				list_countries_to_process.append(one_country)
			else:
				print(one_country + ' not found in the available countries list.')
	else:
		print("Country not found, please check the available countries in the following list.")
		print(get_list_countries_available(DATA_PATH))
	return list_countries_to_process

def get_world_data(data):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		dictionnary_data_world = {}
		for line in f_o:
			if line[1] == 'World':
				dictionnary_data_world[line[0]] = line[2] + ',' + line[3] + ',' + line[4] + ',' + line[5]
	return dictionnary_data_world