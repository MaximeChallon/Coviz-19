import os
import csv
from .constantes import *
import datetime
import matplotlib.pyplot as plt
import json
import pandas as pd


DATA_PATH = "utilitaires/data/data_full.csv"


def clean_folder():
	try:
		os.remove('full_data.csv')
	except:
		pass

	try:
		os.remove('full_data_with_pop.csv')
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
	elif liste != [] :
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


def get_world_data(data, country):
	with open(data, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		dictionnary_data_world = {}
		for line in f_o:
			if line[1] == country:
				dictionnary_data_world[line[0]] = line[2] + ',' + line[3] + ',' + line[4] + ',' + line[5] + ',' + line[6] + ',' + line[7] + ',' + line[8] + ',' + line[9]
	return dictionnary_data_world


def simple_plot_world(message, name_img, index, y_label, output_folder, world_dictionnary):
	print(message)
	img_path = output_folder + name_img
	fig = plt.figure(figsize=MORE_30D)
	plt.xticks(rotation=90)
	ax = plt.subplot()
	ax.plot([day for day in world_dictionnary], [float(world_dictionnary[day].split(',')[index]) for day in world_dictionnary], COLOR, linewidth=2.5)
	ax.set_xlabel('Date')
	ax.set_ylabel(y_label)
	ax.yaxis.grid(True)
	ax.margins(0, 0)
	plt.tight_layout()
	plt.savefig(img_path)
	plt.close(fig)


def get_csv_world(output_folder, csv_path, index, world_dictionnary, country):
	with open(csv_path, 'w') as f:
		writer = csv.writer(f)
		print("Writing headers...")
		if index == 0:
			header = "cases_of_the_day"
		elif index == 1 :
			header = "deaths_of_the_day"
		elif index == 2:
			header = "total_cases"
		elif index == 3:
			header = "total_deaths"
		elif index == 4:
			header = "cases_of_the_day_per_10000"
		elif index == 5:
			header = "deaths_of_the_day_per_10000"
		elif index == 6:
			header = "total_cases_per_10000"
		elif index == 7:
			header = "total_deaths_per_10000"
		writer.writerow(["country", "date", header])
		print("Writing the body...")
		for day in world_dictionnary:
			data_split = world_dictionnary[day].split(',')
			writer.writerow([country, day, data_split[index]])


def get_csv_today(output_folder, csv_path, index, country, full, liste):
	csv_path = output_folder + '/' + csv_path
	with open(csv_path, 'w') as f:
			writer = csv.writer(f)
			print('Writing headers...')
			if index == 0:
				header = "cases_of_the_day"
			elif index == 1 :
				header = "deaths_of_the_day"
			elif index == 2:
				header = "total_cases"
			elif index == 3:
				header = "total_deaths"
			writer.writerow(["country", header])
			for country in get_list_countries_to_process(country=country, full=full, liste=liste):
				print(country + ' on process...')
				if country in get_data_today(DATA_PATH):
					writer.writerow([country, get_data_today(DATA_PATH)[country][index]])


def simple_plot_country(img_path, index, country, full, liste, output_folder):
	img_path1 = output_folder + '/' + img_path
	fig = plt.figure()
	fig, ax = plt.subplots(1,figsize=MORE_30D)
	plt.xticks(rotation=90)

	# open the json file with dates of quarantine
	json_file = open('utilitaires/data/data_confinement.json')
	confinement = json.load(json_file)

	dictionnaire_for_plotting = {}
	for country in get_list_countries_to_process(country=country, full=full, liste=liste):
		list_country = []
		with open(DATA_PATH, 'r') as f:
			f_o = csv.reader(f)
			next(f_o)
			for line in f_o:
				if line[1] == country:
					list_country.append([line[0], line[index]])
		dictionnaire_for_plotting[country] = list_country


	dates_conf = []
	dates_deconf = []
	value_at_date_conf = []
	value_at_date_deconf = []

	# création d'une courbe par pays donné
	for country in dictionnaire_for_plotting:
		dates_country = []
		data_country = []
		for data in dictionnaire_for_plotting[country]:
			date, data = data
			dates_country.append(date)
			data_country.append(float(data))
		ax.plot(dates_country, data_country, label=country, linewidth=2.5)

		# ajout des points de confinement et de déconfinement
		for date in dates_country:
			if country in confinement["beginning"]:
				if date == confinement["beginning"][country]:
					dates_conf.append(date)
					value_at_date_conf.append(data_country[dates_country.index(date)])
			if country in confinement["end"]:
				if date == confinement["end"][country]:
					dates_deconf.append(date)
					value_at_date_deconf.append(data_country[dates_country.index(date)])
	
	if dates_conf != []:
		ax.scatter(dates_conf, value_at_date_conf, s=140, c="r", marker='X', label="Confinement")
	if dates_deconf != []:
		ax.scatter(dates_deconf, value_at_date_deconf, s=140, c="g", marker='X', label="Déconfinement")


	ax.set_xlabel('Date', fontsize=16)
	ax.set_ylabel(img_path.replace('.png', '').replace('out/', '').replace('_', ' '), fontsize=16)
	ax.yaxis.grid(True)
	plt.margins(0, 0)
	plt.tight_layout()
	plt.legend(loc="upper left", title="Countries", title_fontsize=18, fontsize=16)
	plt.savefig(img_path1)
	plt.close(fig)

	json_file.close()

def calcul_par_10000_hbts():
	DATA = 'wget https://covid.ourworldindata.org/data/ecdc/full_data.csv'
	DATA_BEGINNING = 'full_data.csv'
	try:
		os.remove('utilitaires/data/data_full.csv')
	except:
		pass
	
	csv_pop = pd.read_csv('utilitaires/data/data_population.csv')
	df_pop = pd.DataFrame(csv_pop)
	
	csv_df = pd.read_csv(DATA_BEGINNING)
	df_fd = pd.DataFrame(csv_df)
	
	result = pd.merge(df_fd, df_pop, on='location', how='left')
	result.to_csv('utilitaires/data/test.csv' , columns =['date','location','new_cases','new_deaths','total_cases','total_deaths','Population'])
	
	with open('utilitaires/data/test.csv', 'r') as f:
		r = csv.reader(f)
		next(r)
		with open('utilitaires/data/data_full.csv', 'a') as f_e:
			writer = csv.writer(f_e)
			writer.writerow(["date", "location", "new_cases", "new_deaths", "total_cases", "total_deaths", "new_cases_per_10000", "new_deaths_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
			for line in r:
				if line[7] != '':
					total_deaths_per_10000 = int(line[6]) * 10000 / float(line[7])
					deaths_day_per_10000 = int(line[4]) * 10000 / float(line[7])
					total_cases_per_10000 = int(line[5]) * 10000 / float(line[7])
					cases_day_per_10000 = int(line[3]) * 10000 / float(line[7])
					writer.writerow([line[1], line[2], line[3], line[4], line[5], line[6], cases_day_per_10000, deaths_day_per_10000, total_cases_per_10000, total_deaths_per_10000])
				else:
					writer.writerow([line[1], line[2], line[3], line[4], line[5], 0, 0, 0, 0])
	
	os.remove('utilitaires/data/test.csv')
	os.remove(DATA_BEGINNING)	