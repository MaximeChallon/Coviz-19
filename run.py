import click
from utilitaires.fonctions import *
import os
import time
import csv
from utilitaires.constantes import *
from utilitaires.map import *
import matplotlib.pyplot as plt
import folium
import pandas as pd

clean_folder()

DATA = 'wget https://covid.ourworldindata.org/data/ecdc/full_data.csv'
DATA_BEGINNING = 'full_data.csv'
DATA_PATH = 'utilitaires/data/data_full.csv'

@click.group(context_settings={'help_option_names':['-h','--help']})
def main():
    pass


@main.command("plot")
@click.argument("output_folder",
              default="out")
@click.option("-c", 
	'--country' ,
	help='Execute the command for the country')
@click.option("-f", 
	"--full", 
	is_flag=True, 
	help="Execute the command for all the countries")
@click.option("-l", 
	"--liste", 
	default=[],
	help="Execute the command for a list of countries")
@click.option('-ptd',
	'--plot_total_deaths',
	is_flag=True,
	help="Create a PNG plot with the data of cumulative deaths of the given country(ies)")
@click.option('-pdd',
	'--plot_deaths_of_the_day',
	is_flag=True,
	help="Create a PNG plot with the data of the deaths of the day of the given country(ies)")
@click.option('-ptc',
	'--plot_total_cases',
	is_flag=True,
	help="Create a PNG plot with the data of cumulative cases of the given country(ies)")
@click.option('-pcd',
	'--plot_cases_of_the_day',
	is_flag=True,
	help="Create a PNG plot with the data of the cases of the day of the given country(ies)")
@click.option('-pcdpi',
	'--plot_cases_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cases of the day per 10000 inhabitants of the given country(ies)")
@click.option('-pddpi',
	'--plot_deaths_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the deaths of the day per 10000 inhabitants of the given country(ies)")
@click.option('-ptcpi',
	'--plot_total_cases_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cumulative cases per 10000 inhabitants of the given country(ies)")
@click.option('-ptdpi',
	'--plot_total_deaths_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cumulative deaths per 10000 inhabitants of the given country(ies)")
def plot(output_folder, country, full, liste, 
	plot_total_deaths, plot_deaths_of_the_day, plot_total_cases, plot_cases_of_the_day,
	plot_cases_of_the_day_per_10000_inhabitants, plot_deaths_of_the_day_per_10000_inhabitants, plot_total_deaths_per_10000_inhabitants, plot_total_cases_per_10000_inhabitants):
	"""
	Create PNG plot for the data of the given country(ies)
	\f
	:param country: name of a country, with a capital letter at the beginning
	:type country: str
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param full: if given, all the countries available are process
	:type full: bool
	:param liste: list of countries to be process
	:type liste: list
	:param plot_total_deaths: PNG plot with data of the cumulative deaths of the given country(ies)
	:type plot_total_deaths: bool
	:param plot_deaths_of_the_day: PNG plot with data of the deaths of the day of the given country(ies)
	:type plot_deaths_of_the_day: bool
	:param plot_total_cases: PNG plot with data of the cumulative cases of the given country(ies)
	:type plot_total_cases: bool
	:param plot_cases_of_the_day: PNG plot with data of the cases of the day of the given country(ies)
	:type plot_cases_of_the_day: bool
	:param plot_cases_of_the_day_per_10000_inhabitants: PNG plot with data of the cases of the day per 10000 inhabitants of the given country(ies)
	:type plot_cases_of_the_day: bool
	:param plot_deaths_of_the_day_per_10000_inhabitants: PNG plot with data of the deaths of the day per 10000 inhabitants of the given country(ies)
	:type plot_deaths_of_the_day: bool
	:param plot_total_cases_per_10000_inhabitants: PNG plot with data of the cumulative cases per 10000 inhabitants of the given country(ies)
	:type plot_total_cases_per_10000_inhabitants: bool
	:param plot_total_deaths_per_10000_inhabitants: PNG plot with data of the cumulative deaths per 10000 inhabitants of the given country(ies)
	:type plot_total_deaths_per_10000_inhabitants: bool
	:return: nothing
	:rtype: None
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	# managing the folders...
	os.system('mkdir ' + output_folder)

	if plot_total_deaths:
		simple_plot_country(index=5, img_path='plot_total_deaths.png', country=country, full=full, liste=liste, output_folder=output_folder)
	elif plot_deaths_of_the_day:
		simple_plot_country(index=3, img_path='plot_deaths_of_the_day.png', country=country, full=full, liste=liste, output_folder=output_folder)
	elif plot_total_cases:
		simple_plot_country(index=4, img_path='plot_total_cases.png', country=country, full=full, liste=liste, output_folder=output_folder)
	elif plot_cases_of_the_day:
		simple_plot_country(index=2, img_path='plot_cases_of_the_day.png', country=country, full=full, liste=liste, output_folder=output_folder)
	elif plot_cases_of_the_day_per_10000_inhabitants:
		simple_plot_country(index=6, img_path='plot_cases_of_the_day_per_10000_inhabitants.png', full=full, liste=liste, country=country, output_folder=output_folder)
	elif plot_deaths_of_the_day_per_10000_inhabitants:
		simple_plot_country(index=7, img_path='plot_deaths_of_the_day_per_10000_inhabitants.png', full=full, liste=liste, country=country, output_folder=output_folder)
	elif plot_total_deaths_per_10000_inhabitants:
		simple_plot_country(index=9, img_path='plot_total_deaths_per_10000_inhabitants.png', full=full, liste=liste, country=country, output_folder=output_folder)
	elif plot_total_cases_per_10000_inhabitants:
		simple_plot_country(index=8, img_path='plot_total_cases_per_10000_inhabitants.png', full=full, liste=liste, country=country, output_folder=output_folder)

	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


@main.command("world")
@click.argument("output_folder",
              default="out")
@click.option('-t',
	'--today',
	is_flag=True,
	help="Process the data of today")
@click.option('-f',
	'--full',
	is_flag=True,
	help='Process all the data from all the dates available')
@click.option('-cf',
	'--csv_full',
	is_flag=True,
	help='Create a CSV file as output with all data')
@click.option('-cdd',
	'--csv_deaths_of_the_day',
	is_flag=True,
	help='Create a CSV file as output with the deaths of the day')
@click.option('-ctd',
	'--csv_total_deaths',
	is_flag=True,
	help='Create a CSV file as output with the cumulative deaths')
@click.option('-ctc',
	'--csv_total_cases',
	is_flag=True,
	help='Create a CSV file as output with the cumulative cases')
@click.option('-ccd',
	'--csv_cases_of_the_day',
	is_flag=True,
	help='Create a CSV file as output with the cases of the day')
@click.option('-ccdpi',
	'--csv_cases_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a CSV file with the data of the cases of the day per 10000 inhabitants of the given country(ies)")
@click.option('-cddpi',
	'--csv_deaths_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a CSV file with the data of the deaths of the day per 10000 inhabitants of the given country(ies)")
@click.option('-ctcpi',
	'--csv_total_cases_per_10000_inhabitants',
	is_flag=True,
	help="Create a CSV file with the data of the cumulative cases per 10000 inhabitants of the given country(ies)")
@click.option('-ctdpi',
	'--csv_total_deaths_per_10000_inhabitants',
	is_flag=True,
	help="Create a CSV file with the data of the cumulative deaths per 10000 inhabitants of the given country(ies)")
@click.option('-pf',
	'--plot_full',
	is_flag=True,
	help='Create all the 4 plots available')
@click.option('-pdd',
	'--plot_deaths_of_the_day',
	is_flag=True,
	help='Create a PNG plot from the deaths of the day')
@click.option('-pcd',
	'--plot_cases_of_the_day',
	is_flag=True,
	help='Create a PNG plot from the cases of the day')
@click.option('-ptd',
	'--plot_total_deaths',
	is_flag=True,
	help='Create a PNG plot from the cumulative deaths')
@click.option('-ptc',
	'--plot_total_cases',
	is_flag=True,
	help='Create a PNG plot from the cumulative cases')
@click.option('-pcdpi',
	'--plot_cases_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cases of the day per 10000 inhabitants of the given country(ies)")
@click.option('-pddpi',
	'--plot_deaths_of_the_day_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the deaths of the day per 10000 inhabitants of the given country(ies)")
@click.option('-ptcpi',
	'--plot_total_cases_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cumulative cases per 10000 inhabitants of the given country(ies)")
@click.option('-ptdpi',
	'--plot_total_deaths_per_10000_inhabitants',
	is_flag=True,
	help="Create a PNG plot with the data of the cumulative deaths per 10000 inhabitants of the given country(ies)")
def world(output_folder, today, full, 
	csv_full, csv_deaths_of_the_day, csv_total_deaths, csv_total_cases, csv_cases_of_the_day,
	csv_cases_of_the_day_per_10000_inhabitants, csv_deaths_of_the_day_per_10000_inhabitants, csv_total_cases_per_10000_inhabitants, csv_total_deaths_per_10000_inhabitants, 
	plot_full, plot_deaths_of_the_day, plot_cases_of_the_day, plot_total_deaths, plot_total_cases,
	plot_cases_of_the_day_per_10000_inhabitants, plot_deaths_of_the_day_per_10000_inhabitants, plot_total_cases_per_10000_inhabitants, plot_total_deaths_per_10000_inhabitants):
	"""
	Create a CSV file or a PNG image from the world's data of today or all the available dates.
	\f
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param today: if given, only the data of the day are using in the process
	:type today: bool
	:param full: if given, all the data are using in the process
	:type full: bool
	:param csv_full: if given, create a CSV file as output
	:type csv_full: bool
	:param csv_deaths_of_the_day: if given, create a CSV file as output with deaths of the day's data
	:type csv_deaths_of_the_day: bool
	:param csv_cases_of_the_day: if given, create a CSV file as output with cases of the day's data
	:type csv_cases_of_the_day: bool
	:param csv_total_deaths: if given, create a CSV file as output with the cumulative deaths's data
	:type csv_total_deaths: bool
	:param csv_total_cases: if given, create a CSV file as output with the cumulative cases's data
	:type csv_total_cases: bool
	:param plot_full: if given, create 4 PNG plots
	:param csv_cases_of_the_day_per_10000_inhabitants: if given, CSV file with data of the cases of the day per 10000 inhabitants of the given country(ies)
	:type csv_cases_of_the_day: bool
	:param csv_deaths_of_the_day_per_10000_inhabitants: if given, CSV file with data of the deaths of the day per 10000 inhabitants of the given country(ies)
	:type csv_deaths_of_the_day: bool
	:param csv_total_cases_per_10000_inhabitants: if given, CSV file with data of the cumulative cases per 10000 inhabitants of the given country(ies)
	:type csv_total_cases_per_10000_inhabitants: bool
	:param csv_total_deaths_per_10000_inhabitants: if given, CSV file with data of the cumulative deaths per 10000 inhabitants of the given country(ies)
	:type csv_total_deaths_per_10000_inhabitants: bool
	:type plot_full: bool
	:param plot_deaths_of_the_day: if given, create a PNG image as output for the deaths of the day
	:type plot_deaths_of_the_day: bool
	:param plot_cases_of_the_day: if given, create a PNG image as output for the cases of the day
	:type plot_cases_of_the_day: bool
	:param plot_total_deaths: if given, create a PNG image as output for the total of deaths
	:type plot_total_deaths: bool
	:param plot_total_cases: if given, create a PNG image as output for the total of cases
	:type plot_total_cases: bool
	:param plot_cases_of_the_day_per_10000_inhabitants: if given, PNG plot with data of the cases of the day per 10000 inhabitants of the given country(ies)
	:type plot_cases_of_the_day: bool
	:param plot_deaths_of_the_day_per_10000_inhabitants: if given, PNG plot with data of the deaths of the day per 10000 inhabitants of the given country(ies)
	:type plot_deaths_of_the_day: bool
	:param plot_total_cases_per_10000_inhabitants: if given, PNG plot with data of the cumulative cases per 10000 inhabitants of the given country(ies)
	:type plot_total_cases_per_10000_inhabitants: bool
	:param plot_total_deaths_per_10000_inhabitants: if given, PNG plot with data of the cumulative deaths per 10000 inhabitants of the given country(ies)
	:type plot_total_deaths_per_10000_inhabitants: bool
	:return: nothing
	:rtype: None
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	# managing the folders...
	os.system('mkdir ' + output_folder)

	world_dictionnary = {}
	if today:
		try:
			world_dictionnary[TODAY] = get_world_data(DATA_PATH, 'World')[TODAY]
		except:
			world_dictionnary[YESTERDAY_CUT] = get_world_data(DATA_PATH, 'World')[YESTERDAY_CUT]
	elif full:
		world_dictionnary = get_world_data(DATA_PATH, 'World')
	
	if csv_full:
		csv_path = output_folder + "/world_full.csv"
		with open(csv_path, 'w') as f:
			writer = csv.writer(f)
			print("Writing headers...")
			writer.writerow(["date", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths", "new_cases_per_10000", "new_deaths_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
			print("Writing the body...")
			for day in world_dictionnary:
				data_split = world_dictionnary[day].split(',')
				writer.writerow([day, data_split[0], data_split[1], data_split[2], data_split[3], data_split[4], data_split[5], data_split[6], data_split[7]])
	elif csv_deaths_of_the_day:
		get_csv_world(output_folder, output_folder + "/world_deaths_of_the_day.csv", 1, world_dictionnary, "World")
	elif csv_total_deaths:
		get_csv_world(output_folder, output_folder + "/world_total_deaths.csv", 3, world_dictionnary, "World")
	elif csv_total_cases:
		get_csv_world(output_folder, output_folder + "/world_total_cases.csv", 2, world_dictionnary, "World")
	elif csv_cases_of_the_day:
		get_csv_world(output_folder, output_folder + "/world_cases_of_the_day.csv", 0, world_dictionnary, "World")
	elif csv_cases_of_the_day_per_10000_inhabitants:
		get_csv_world(output_folder, output_folder + "/world_cases_of_the_day_per_10000_inhabitants.csv", 4, world_dictionnary, "World")
	elif csv_deaths_of_the_day_per_10000_inhabitants:
		get_csv_world(output_folder, output_folder + "/world_deaths_of_the_day_per_10000_inhabitants.csv", 5, world_dictionnary, "World")
	elif csv_total_cases_per_10000_inhabitants:
		get_csv_world(output_folder, output_folder + "/world_total_cases_per_10000_inhabitants.csv", 6, world_dictionnary, "World")
	elif csv_total_deaths_per_10000_inhabitants:
		get_csv_world(output_folder, output_folder + "/world_total_deaths_per_10000_inhabitants.csv", 7, world_dictionnary, "World")
	elif plot_full:
		simple_plot_world("Creating plot with deaths of the day...", "/world_deaths_of_the_day.png", 1, "Nombre de décès quotidiens", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with cases of the day...", "/world_cases_of_the_day.png", 0, "Nombre de cas quotidiens", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with total deaths...", "/world_total_deaths.png", 3, "Nombre total de décès", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with total cases...", "/world_total_cases.png", 2, "Nombre total de cas", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with cases of the day per 10000 inhabitants...", "/world_cases_of_the_day_per_10000_inhabitants.png", 4, "Nombre de cas quotidiens pour 10000 habitants", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with total cases per 10000 inhabitants...", "/world_total_cases_per_10000_inhabitants.png", 6, "Nombre total de cas pour 10000 habitants", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with deaths of the day per 10000 inhabitants...", "/world_deaths_of_the_day_per_10000_inhabitants.png", 5, "Nombre de décès quotidiens pour 10000 habitants", output_folder, world_dictionnary)
		simple_plot_world("Creating plot with total deaths per 10000 inhabitants...", "/world_total_deaths_per_10000_inhabitants.png", 7, "Nombre total de décès pour 10000 habitants", output_folder, world_dictionnary)
	elif plot_deaths_of_the_day:
		simple_plot_world("Creating plot with deaths of the day...", "/world_deaths_of_the_day.png", 1, "Nombre de décès quotidiens", output_folder, world_dictionnary)
	elif plot_cases_of_the_day:
		simple_plot_world("Creating plot with cases of the day...", "/world_cases_of_the_day.png", 0, "Nombre de cas quotidiens", output_folder, world_dictionnary)
	elif plot_total_deaths:
		simple_plot_world("Creating plot with total deaths...", "/world_total_deaths.png", 3, "Nombre total de décès", output_folder, world_dictionnary)
	elif plot_total_cases:
		simple_plot_world("Creating plot with total cases...", "/world_total_cases.png", 2, "Nombre total de cas", output_folder, world_dictionnary)
	elif plot_cases_of_the_day_per_10000_inhabitants:
		simple_plot_world("Creating plot with cases of the day per 10000 inhabitants...", "/world_cases_of_the_day_per_10000_inhabitants.png", 4, "Nombre de cas quotidiens pour 10000 habitants", output_folder, world_dictionnary)
	elif plot_deaths_of_the_day_per_10000_inhabitants:
		simple_plot_world("Creating plot with deaths of the day per 10000 inhabitants...", "/world_deaths_of_the_day_per_10000_inhabitants.png", 5, "Nombre de décès quotidiens pour 10000 habitants", output_folder, world_dictionnary)
	elif plot_total_cases_per_10000_inhabitants:
		simple_plot_world("Creating plot with total cases per 10000 inhabitants...", "/world_total_cases_per_10000_inhabitants.png", 6, "Nombre total de cas pour 10000 habitants", output_folder, world_dictionnary)
	elif plot_total_deaths_per_10000_inhabitants:
		simple_plot_world("Creating plot with total deaths per 10000 inhabitants...", "/world_total_deaths_per_10000_inhabitants.png", 7, "Nombre total de décès pour 10000 habitants", output_folder, world_dictionnary)
	else:
		print("Please specify the output")
		print(os.system('python3 run.py world -h'))

	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


@main.command("today")
@click.argument("output_folder",
              default="out")
@click.option("-c", 
	'--country' ,
	help='Execute the command for the country')
@click.option("-f", 
	"--full", 
	is_flag=True, 
	help="Execute the command for all the countries")
@click.option("-l", 
	"--liste", 
	default=[],
	help="Execute the command for a list of countries")
@click.option("-td", 
	"--total_deaths", 
	is_flag=True,
	help="Process the cumulative deaths")
@click.option("-cd", 
	"--cases_of_the_day", 
	is_flag=True,
	help="Process the cases of the day")
@click.option("-dd", 
	"--deaths_of_the_day", 
	is_flag=True,
	help="Process the deaths of the day")
@click.option("-tc", 
	"--total_cases", 
	is_flag=True,
	help="Process the cumulative cases")
@click.option("-cdpi", 
	"--cases_of_the_day_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cases of the day per 10000 inhabitants")
@click.option("-ddpi", 
	"--deaths_of_the_day_per_10000_inhabitants", 
	is_flag=True,
	help="Process the deaths of the day per 10000 inhabitants")
@click.option("-tcpi", 
	"--total_cases_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cumulative cases per 10000 inhabitants")
@click.option("-tdpi", 
	"--total_deaths_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cumulative deaths per 10000 inhabitants")
def country(country, output_folder, full, liste, 
	total_deaths, total_cases, cases_of_the_day, deaths_of_the_day,
	cases_of_the_day_per_10000_inhabitants, deaths_of_the_day_per_10000_inhabitants, total_cases_per_10000_inhabitants, total_deaths_per_10000_inhabitants):
	"""
	Create a CSV file with today's data for today's deaths, total deaths, today's cases, total cases for the country(ies) given in parameter.
	\f
	:param country: name of a country, with a capital letter at the beginning
	:type country: str
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param full: if given, all the countries available are process
	:type full: bool
	:param liste: list of countries to be process
	:type liste: list
	:param total_deaths: if given, create a CSV for the total of the deaths
	:type total_deaths: bool
	:param total_cases: if given, create a CSV for the total of the cases
	:type total_cases: bool
	:param deaths_of_the_day: if given, create a CSV for the deaths of the day
	:type deaths_of_the_day: bool
	:param cases_of_the_day: if given, create a CSV for the cases of the day
	:type cases_of_the_day: bool
	:param cases_of_the_day_per_10000_inhabitants: if given, create a CSV for the cases of the day per 10000 inhabitants
	:type cases_of_the_day_per_10000_inhabitants: bool
	:param deaths_of_the_day_per_10000_inhabitants: if given, create a CSV for the deaths of the day per 10000 inhabitants
	:type deaths_of_the_day_per_10000_inhabitants: bool
	:param total_cases_per_10000_inhabitants: if given, create a CSV for the cumulative cases per 10000 inhabitants
	:type total_cases_per_10000_inhabitants: bool
	:param total_deaths_per_10000_inhabitants: if given, create a CSV for the cumulative deaths per 10000 inhabitants
	:type total_deaths_per_10000_inhabitants: bool
	:return: nothing
	:rtype: None
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	# managing the folders...
	os.system('mkdir ' + output_folder)	

	if total_deaths:
		get_csv_today(output_folder, '/today_total_deaths.csv', 3, country=country, full=full, liste=liste)
	elif total_cases:
		get_csv_today(output_folder, '/today_total_cases.csv', 2, country=country, full=full, liste=liste)
	elif cases_of_the_day:
		get_csv_today(output_folder, '/today_cases_of_the_day.csv', 0, country=country, full=full, liste=liste)
	elif deaths_of_the_day:
		get_csv_today(output_folder, '/today_deaths_of_the_day.csv', 1, country=country, full=full, liste=liste)
	elif cases_of_the_day_per_10000_inhabitants:
		get_csv_today(output_folder, '/today_cases_of_the_day_per_10000_inhabitants.csv', 4, country=country, full=full, liste=liste)
	elif deaths_of_the_day_per_10000_inhabitants:
		get_csv_today(output_folder, '/today_deaths_of_the_day_per_10000_inhabitants.csv', 5, country=country, full=full, liste=liste)
	elif total_cases_per_10000_inhabitants:
		get_csv_today(output_folder, '/today_total_cases_per_10000_inhabitants.csv', 6, country=country, full=full, liste=liste)
	elif total_deaths_per_10000_inhabitants:
		get_csv_today(output_folder, '/today_total_deaths_per_10000_inhabitants.csv', 7, country=country, full=full, liste=liste)
	else: # create a CSV with all the data 
		csv_path = output_folder + '/today_all_data.csv'
		with open(csv_path, 'w') as f:
			writer = csv.writer(f)
			print('Writing headers...')
			writer.writerow(["country", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths", "new_cases_per_10000", "new_deaths_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
			for country in get_list_countries_to_process(country=country, full=full, liste=liste):
				print(country + ' on process...')
				if country in get_data_today(DATA_PATH):
					writer.writerow([country, get_data_today(DATA_PATH)[country][0], get_data_today(DATA_PATH)[country][1], get_data_today(DATA_PATH)[country][2], get_data_today(DATA_PATH)[country][3], get_data_today(DATA_PATH)[country][4], get_data_today(DATA_PATH)[country][5], get_data_today(DATA_PATH)[country][6], get_data_today(DATA_PATH)[country][7]])

	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


@main.command("csv_country")
@click.argument("output_folder", 
	default="out")
@click.option("-c", 
	'--country' ,
	help="Execute the command for the country")
@click.option("-f", 
	"--full", 
	is_flag=True,
	help="Execute the command for all the countries")
@click.option("-l", 
	"--liste", 
	default=[],
	help="Execute the command for a list of countries")
def country_to_csv (country, output_folder, full, liste):
	"""
	Create a CSV file for each country given in parameter.
	\f
	:param country: name of a country, with a capital letter at the beginning
	:type country: str
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param full: if given, a CSV file is create for each country available
	:type full: bool
	:param liste: list of countries to be process
	:type liste: list
	:return: nothing
	:rtype: None
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	# managing the folders...
	folder_path = output_folder + '/countries'
	os.system('mkdir ' + output_folder)
	os.system('mkdir ' + output_folder + '/countries')

	for country in get_list_countries_to_process(country=country, full=full, liste=liste):
		print(country + ' on process...')
		# creation of one folder for each country
		os.system('mkdir ' + folder_path + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_'))
		csv_path = folder_path + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '/' +  country.replace(')', '_').replace('(', '_').replace(' ', '_').replace('\'', '_') + '.csv'

		with open(DATA_PATH, 'r') as f:
			f_o = csv.reader(f)
			next(f_o)
			with open(csv_path, 'a') as f_e:
				writer = csv.writer(f_e)
				print("Writing headers...")
				writer.writerow(["date", "country", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths", "new_cases_per_10000", "new_deaths_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
				print("Writing body...")
				for line in f_o:
					# écriture des lignes que quand le nombre de cas est supérieur à PLOT_MIN_CASES
					if line[1] == country and line[4] >= PLOT_MIN_CASES:
						writer.writerow(line)

	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


@main.command("country")
@click.argument("output_folder", 
	default="out")
@click.argument("country")
@click.option('-td',
	'--total_deaths',
	is_flag=True,
	help="Process the cumulative deaths data")
@click.option('-tc',
	'--total_cases',
	is_flag=True,
	help="Process the cumulative cases data")
@click.option('-cd',
	'--cases_of_the_day',
	is_flag=True,
	help="Process the cases of the day data")
@click.option('-dd',
	'--deaths_of_the_day',
	is_flag=True,
	help="Process the deaths of the day data")
@click.option("-cdpi", 
	"--cases_of_the_day_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cases of the day per 10000 inhabitants")
@click.option("-ddpi", 
	"--deaths_of_the_day_per_10000_inhabitants", 
	is_flag=True,
	help="Process the deaths of the day per 10000 inhabitants")
@click.option("-tcpi", 
	"--total_cases_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cumulative cases per 10000 inhabitants")
@click.option("-tdpi", 
	"--total_deaths_per_10000_inhabitants", 
	is_flag=True,
	help="Process the cumulative deaths per 10000 inhabitants")
@click.option('-fd',
	'--full_data',
	is_flag=True,
	help="Process all the available data")
@click.option('-c',
	'--csv_o',
	is_flag=True,
	help="Create a CSV file in output")
@click.option('-p',
	'--plot',
	is_flag=True,
	help="Create a PNG plot in output")
@click.option('-fo',
	'--full_outputs',
	is_flag=True,
	help="Create CSV files and PNG plots in output")
def country(output_folder, country, 
	total_deaths, total_cases, cases_of_the_day, deaths_of_the_day,
	cases_of_the_day_per_10000_inhabitants, deaths_of_the_day_per_10000_inhabitants, total_deaths_per_10000_inhabitants, total_cases_per_10000_inhabitants,
	full_data, full_outputs, csv_o, plot):
	"""
	For the given country, create CSV files or PNG plots for the given data.
	\f
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param country: name of a country, with a capital letter at the beginning
	:type country: str
	:param total_deaths: if given, the total deaths data are process
	:type total_deaths: bool
	:param total_cases: if given, the total cases data are process
	:type total_cases: bool
	:param cases_of_the_day: if given, the cases of the day data are process
	:type cases_of_the_day: bool
	:param deaths_of_the_day: if given, the deaths of the day data are process
	:type deaths_of_the_day: bool
	:param cases_of_the_day_per_10000_inhabitants: if given, create a CSV for the cases of the day per 10000 inhabitants
	:type cases_of_the_day_per_10000_inhabitants: bool
	:param deaths_of_the_day_per_10000_inhabitants: if given, create a CSV for the deaths of the day per 10000 inhabitants
	:type deaths_of_the_day_per_10000_inhabitants: bool
	:param total_cases_per_10000_inhabitants: if given, create a CSV for the cumulative cases per 10000 inhabitants
	:type total_cases_per_10000_inhabitants: bool
	:param total_deaths_per_10000_inhabitants: if given, create a CSV for the cumulative deaths per 10000 inhabitants
	:type total_deaths_per_10000_inhabitants: bool
	:param full_data: if given, process all the available data of the country
	:type full_data: bool
	:param full_outputs: if given, create CSV and PNG files
	:type full_ouptuts: bool
	:param csv: if given, a CSV file is created
	:type csv: bool
	:return: nothing
	:rtype: None
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	# managing the folders...
	os.system('mkdir ' + output_folder)	

	world_dictionnary = {}
	with open(DATA_PATH, 'r') as f:
		f_o = csv.reader(f)
		next(f_o)
		for line in f_o:
			if line[1] == country:
				world_dictionnary[line[0]]=get_world_data(DATA_PATH, country)[line[0]]

	if csv_o:
		if total_deaths:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths.csv'
			get_csv_world(output_folder, csv_path, 3, world_dictionnary, country)
		elif total_cases:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases.csv'
			get_csv_world(output_folder, csv_path, 2, world_dictionnary, country)
		elif cases_of_the_day:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day.csv'
			get_csv_world(output_folder, csv_path, 0, world_dictionnary, country)
		elif deaths_of_the_day:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day.csv'
			get_csv_world(output_folder, csv_path, 1, world_dictionnary, country)
		elif cases_of_the_day_per_10000_inhabitants:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day_per_10000_inhabitants.csv'
			get_csv_world(output_folder, csv_path, 4, world_dictionnary, country)
		elif deaths_of_the_day_per_10000_inhabitants:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day_per_10000_inhabitants.csv'
			get_csv_world(output_folder, csv_path, 5, world_dictionnary, country)
		elif total_cases_per_10000_inhabitants:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases_per_10000_inhabitants.csv'
			get_csv_world(output_folder, csv_path, 6, world_dictionnary, country)
		elif total_deaths_per_10000_inhabitants:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths_per_10000_inhabitants.csv'
			get_csv_world(output_folder, csv_path, 7, world_dictionnary, country)
		elif full_data:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_full_data.csv'
			with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print("Writing headers...")
				writer.writerow(["country", "date", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths", "cases_of_the_day_per_10000", "deaths_of_the_day_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
				print("Writing the body...")
				for day in world_dictionnary:
					data_split = world_dictionnary[day].split(',')
					writer.writerow([country, day, data_split[0], data_split[1], data_split[2], data_split[3], data_split[4], data_split[5], data_split[6], data_split[7]])
		elif not total_deaths and not total_cases and not cases_of_the_day and not deaths_of_the_day and not full_data and not cases_of_the_day_per_10000_inhabitants and not deaths_of_the_day_per_10000_inhabitants and not total_cases_per_10000_inhabitants and not total_deaths_per_10000_inhabitants:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_full_data.csv'
			with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print("Writing headers...")
				writer.writerow(["country", "date", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths", "cases_of_the_day_per_10000", "deaths_of_the_day_per_10000","total_cases_per_10000", "total_deaths_per_10000"])
				print("Writing the body...")
				for day in world_dictionnary:
					data_split = world_dictionnary[day].split(',')
					writer.writerow([country, day, data_split[0], data_split[1], data_split[2], data_split[3], data_split[4], data_split[5], data_split[6], data_split[7]])
	
	elif plot:
		if total_deaths:
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths.png' 
			simple_plot_country(img_path, 5, country, full=False, liste=[], output_folder=output_folder)
		elif total_cases:
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases.png' 
			simple_plot_country(img_path, 4, country, full=False, liste=[], output_folder=output_folder)
		elif cases_of_the_day:
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day.png' 
			simple_plot_country(img_path, 2, country, full=False, liste=[], output_folder=output_folder)
		elif deaths_of_the_day:
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day.png' 
			simple_plot_country(img_path, 3, country, full=False, liste=[], output_folder=output_folder)
		elif cases_of_the_day_per_10000_inhabitants:
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day_per_10000_inhabitants.png' 
			simple_plot_country(img_path, 6, country, full=False, liste=[], output_folder=output_folder)
		
		elif not total_deaths and not total_cases and not cases_of_the_day and not deaths_of_the_day and not full_data:
			print("Please choose a dataset")
			os.system('python3 run.py country -h')
	
	elif full_outputs:
		if total_deaths:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths.csv'
			get_csv_world(output_folder, csv_path, 3, world_dictionnary, country)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths.png' 
			simple_plot_country(img_path, 5, country, full=False, liste=[], output_folder=output_folder)
		elif total_cases:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases.csv'
			get_csv_world(output_folder, csv_path, 2, world_dictionnary, country)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases.png' 
			simple_plot_country(img_path, 4, country, full=False, liste=[], output_folder=output_folder)
		elif cases_of_the_day:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day.csv'
			get_csv_world(output_folder, csv_path, 0, world_dictionnary, country)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day.png' 
			simple_plot_country(img_path, 2, country, full=False, liste=[], output_folder=output_folder)
		elif deaths_of_the_day:
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day.csv'
			get_csv_world(output_folder, csv_path, 1, world_dictionnary, country)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day.png' 
			simple_plot_country(img_path, 3, country, full=False, liste=[], output_folder=output_folder)
		elif full_data or (not full_data and not total_deaths and not total_cases and not cases_of_the_day and not deaths_of_the_day):
			csv_path = output_folder + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_full_data.csv'
			with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print("Writing headers...")
				writer.writerow(["country", "date", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths"])
				print("Writing the body...")
				for day in world_dictionnary:
					data_split = world_dictionnary[day].split(',')
					writer.writerow([country, day, data_split[0], data_split[1], data_split[2], data_split[3]])
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_deaths.png' 
			simple_plot_country(img_path, 5, country, full=False, liste=[], output_folder=output_folder)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_total_cases.png' 
			simple_plot_country(img_path, 4, country, full=False, liste=[], output_folder=output_folder)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_cases_of_the_day.png' 
			simple_plot_country(img_path, 2, country, full=False, liste=[], output_folder=output_folder)
			img_path = country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '_deaths_of_the_day.png' 
			simple_plot_country(img_path, 3, country, full=False, liste=[], output_folder=output_folder)


	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


@main.command('map')
@click.argument("output_folder", 
	default="out")
@click.option('-mtd',
	'--map_total_deaths',
	is_flag=True,
	help="Create a Leaflet layer with the cumulative deaths data")
@click.option('-mtc',
	'--map_total_cases',
	is_flag=True,
	help="Create a Leaflet layer with the cumulative cases data")
@click.option('-mdd',
	'--map_deaths_of_the_day',
	is_flag=True,
	help="Create a Leaflet layer with the deaths_of_the_day data")
@click.option('-mcd',
	'--map_cases_of_the_day',
	is_flag=True,
	help="Create a Leaflet layer with the cases_of_the_day data")
@click.option('-ptd',
	'--plot_total_deaths',
	is_flag=True,
	help="Create a Vega plot with the cumulative deaths data")
@click.option('-ptc',
	'--plot_total_cases',
	is_flag=True,
	help="Create a Vega plot with the cumulative cases data")
@click.option('-pdd',
	'--plot_deaths_of_the_day',
	is_flag=True,
	help="Create a Vega plot with the deaths_of_the_day data")
@click.option('-pcd',
	'--plot_cases_of_the_day',
	is_flag=True,
	help="Create a Vega plot with the cases_of_the_day data")
@click.option('-pmin',
	'--plot_min',
	help="Define the value of the minimal value to process in the Vega plots")
def map(output_folder, map_total_deaths, map_total_cases, map_deaths_of_the_day, map_cases_of_the_day,
	plot_cases_of_the_day, plot_total_cases, plot_total_deaths, plot_deaths_of_the_day, plot_min):
	"""
	Create a Leaflet map from the data you've given in option. You can add a Vega plot for each country with the same data, or others.
	\f
	:param output_folder: name of the folder which will have the CSVs
	:type output_folder: str
	:param map_total_deaths: if given, create a Leaflet map with the world's cumulative deaths data
	:type map_total_deaths: bool
	:param map_total_cases: if given, create a Leaflet map with the world's cumulative cases data
	:type map_total_cases: bool
	:param map_deaths_of_the_day: if given, create a Leaflet map with the world's deaths of the day data
	:type map_deaths_of_the_day: bool
	:param map_cases_of_the_day: if given, create a Leaflet map with the world's cases of the day data
	:type map_cases_of_the_day: bool
	:param plot_total_deaths: if given, create a Vega plot for each country with the world's cumulative deaths data
	:type plot_total_deaths: bool
	:param plot_total_cases: if given, create a Vega plot for each country with the world's cumulative cases data
	:type plot_total_cases: bool
	:param plot_deaths_of_the_day: if given, create a Vega plot for each country with the world's deaths of the day data
	:type plot_deaths_of_the_day: bool
	:param plot_cases_of_the_day: if given, create a Vega plot for each country with the world's cases of the day data
	:type plot_cases_of_the_day: bool
	:param plot_min: define the value of the minimal value to process in the Vega plots
	:type plot_min: int
	:return: nothing
	:rtype: None 
	"""
	start_time = time.time()

	os.system(DATA)
	calcul_par_10000_hbts()

	if not plot_min:
		plot_min = 5

	if map_deaths_of_the_day or map_cases_of_the_day or map_total_deaths or map_total_cases:
		if map_total_cases:
			if plot_cases_of_the_day:
				map_chloro(index_layer=4, index_plot=2, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_deaths_of_the_day:
				map_chloro(index_layer=4, index_plot=3, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_cases:
				map_chloro(index_layer=4, index_plot=4, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_deaths:
				map_chloro(index_layer=4, index_plot=5, min_plot=int(plot_min), output_folder=output_folder)
			elif not plot_cases_of_the_day and not plot_deaths_of_the_day and not plot_total_deaths and not plot_total_cases:
				map_chloro(index_layer=4, index_plot=4, min_plot=int(plot_min), output_folder=output_folder)
		elif map_total_deaths:
			if plot_cases_of_the_day:
				map_chloro(index_layer=5, index_plot=2, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_deaths_of_the_day:
				map_chloro(index_layer=5, index_plot=3, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_cases:
				map_chloro(index_layer=5, index_plot=4, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_deaths:
				map_chloro(index_layer=5, index_plot=5, min_plot=int(plot_min), output_folder=output_folder)
			elif not plot_cases_of_the_day and not plot_deaths_of_the_day and not plot_total_deaths and not plot_total_cases:
				map_chloro(index_layer=5, index_plot=5, min_plot=int(plot_min), output_folder=output_folder)
		elif map_deaths_of_the_day:
			if plot_cases_of_the_day:
				map_chloro(index_layer=3, index_plot=2, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_deaths_of_the_day:
				map_chloro(index_layer=3, index_plot=3, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_cases:
				map_chloro(index_layer=3, index_plot=4, min_plot=int(plot_min), output_folder=output_folder)
			elif plot_total_deaths:
				map_chloro(index_layer=3, index_plot=5, min_plot=int(plot_min), output_folder=output_folder)
			elif not plot_cases_of_the_day and not plot_deaths_of_the_day and not plot_total_deaths and not plot_total_cases:
				map_chloro(index_layer=3, index_plot=3, min_plot=int(plot_min), output_folder=output_folder)
		elif map_cases_of_the_day:
			if plot_cases_of_the_day:
				map_chloro(index_layer=2, index_plot=2, min_plot=plot_min, output_folder=output_folder)
			elif plot_deaths_of_the_day:
				map_chloro(index_layer=2, index_plot=3, min_plot=plot_min, output_folder=output_folder)
			elif plot_total_cases:
				map_chloro(index_layer=2, index_plot=4, min_plot=plot_min, output_folder=output_folder)
			elif plot_total_deaths:
				map_chloro(index_layer=2, index_plot=5, min_plot=plot_min, output_folder=output_folder)
			elif not plot_cases_of_the_day and not plot_deaths_of_the_day and not plot_total_deaths and not plot_total_cases:
				map_chloro(index_layer=2, index_plot=2, min_plot=plot_min, output_folder=output_folder)

	if not map_deaths_of_the_day and not map_cases_of_the_day and not map_total_deaths and not map_total_cases:
		print("Please give the data you want on the map")
		os.system("python3 run.py map -h")

	os.remove(DATA_PATH)
	print("Execution time : %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()