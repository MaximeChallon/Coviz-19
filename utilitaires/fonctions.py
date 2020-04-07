import os
import csv
from .constantes import *
import datetime
import matplotlib.pyplot as plt
import json


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
				dictionnary_data_world[line[0]] = line[2] + ',' + line[3] + ',' + line[4] + ',' + line[5]
	return dictionnary_data_world


def simple_plot_world(message, name_img, index, y_label, output_folder, world_dictionnary):
	print(message)
	img_path = output_folder + name_img
	fig = plt.figure(figsize=MORE_30D)
	plt.xticks(rotation=45)
	ax = plt.subplot()
	ax.plot([day for day in world_dictionnary], [int(world_dictionnary[day].split(',')[index]) for day in world_dictionnary], COLOR)
	ax.set_xlabel('Date')
	ax.set_ylabel(y_label)
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
	img_path = output_folder + '/' + img_path
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

	for country in dictionnaire_for_plotting:
		dates_country = []
		data_country = []
		for data in dictionnaire_for_plotting[country]:
			date, data = data
			dates_country.append(date)
			data_country.append(int(data))
		ax.plot(dates_country, data_country, label=country)

		for date in dates_country:
			if date == confinement["beginning"][country]:
				value_at_date = data_country[dates_country.index(date)]

		ax.annotate('confinement',
         xy=(confinement["beginning"][country], value_at_date),
         xycoords='data',
         xytext=(confinement["beginning"][country], value_at_date + 130),
         textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1", facecolor='red', edgecolor='red', color='red'))

	ax.set_xlabel('Date')
	ax.set_ylabel(img_path.replace('.png', '').replace('out/', '').replace('_', ' '))
	plt.margins(0, 0)
	plt.tight_layout()
	plt.legend(loc="upper left", title="Countries", frameon=False)
	plt.savefig(img_path)
	plt.close(fig)

	json_file.close()