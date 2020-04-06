import click
from utilitaires.fonctions import *
import os
import time
import csv
from utilitaires.constantes import *

clean_folder()

DATA = os.system('wget https://covid.ourworldindata.org/data/ecdc/full_data.csv')
DATA_PATH = 'full_data.csv'

@click.group(context_settings={'help_option_names':['-h','--help']})
def main():
    pass


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
def world(output_folder, today, full, 
	csv_full, csv_deaths_of_the_day, csv_total_deaths, csv_total_cases, csv_cases_of_the_day, 
	plot_full, plot_deaths_of_the_day, plot_cases_of_the_day, plot_total_deaths, plot_total_cases):
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
	:type plot_full: bool
	:param plot_deaths_of_the_day: if given, create a PNG image as output for the deaths of the day
	:type plot_deaths_of_the_day: bool
	:param plot_cases_of_the_day: if given, create a PNG image as output for the cases of the day
	:type plot_cases_of_the_day: bool
	:param plot_total_deaths: if given, create a PNG image as output for the total of deaths
	:type plot_total_deaths: bool
	:param plot_total_cases: if given, create a PNG image as output for the total of cases
	:type plot_total_cases: bool
	"""
	start_time = time.time()

	# managing the folders...
	os.system('mkdir ' + output_folder)

	world_dictionnary = {}
	if today:
		try:
			world_dictionnary[TODAY] = get_world_data(DATA_PATH)[TODAY]
		except:
			world_dictionnary[YESTERDAY_CUT] = get_world_data(DATA_PATH)[YESTERDAY_CUT]
	elif full:
		world_dictionnary = get_world_data(DATA_PATH)
	
	if csv_full:
		csv_path = output_folder + "/world_full.csv"
		with open(csv_path, 'w') as f:
			writer = csv.writer(f)
			print("Writing headers...")
			writer.writerow(["date", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths"])
			print("Writing the body...")
			for day in world_dictionnary:
				data_split = world_dictionnary[day].split(',')
				writer.writerow([day, data_split[0], data_split[1], data_split[2], data_split[3]])
	elif csv_deaths_of_the_day:
		get_csv(output_folder, "/world_deaths_of_the_day.csv", 1, world_dictionnary)
	elif csv_total_deaths:
		get_csv(output_folder, "/world_total_deaths.csv", 3, world_dictionnary)
	elif csv_total_cases:
		get_csv(output_folder, "/world_total_cases.csv", 2, world_dictionnary)
	elif csv_cases_of_the_day:
		get_csv(output_folder, "/world_cases_of_the_day.csv", 0, world_dictionnary)
	elif plot_full:
		simple_plot("Creating plot with deaths of the day...", "/world_deaths_of_the_day.png", 1, "Nombre de décès quotidiens", output_folder, world_dictionnary)
		simple_plot("Creating plot with cases of the day...", "/world_cases_of_the_day.png", 0, "Nombre de cas quotidiens", output_folder, world_dictionnary)
		simple_plot("Creating plot with total deaths...", "/world_total deaths.png", 3, "Nombre total de décès", output_folder, world_dictionnary)
		simple_plot("Creating plot with total cases...", "/world_total cases.png", 2, "Nombre total de cas", output_folder, world_dictionnary)
	elif plot_deaths_of_the_day:
		simple_plot("Creating plot with deaths of the day...", "/world_deaths_of_the_day.png", 1, "Nombre de décès quotidiens", output_folder, world_dictionnary)
	elif plot_cases_of_the_day:
		simple_plot("Creating plot with cases of the day...", "/world_cases_of_the_day.png", 0, "Nombre de cas quotidiens", output_folder, world_dictionnary)
	elif plot_total_deaths:
		simple_plot("Creating plot with total deaths...", "/world_total deaths.png", 3, "Nombre total de décès", output_folder, world_dictionnary)
	elif plot_total_cases:
		simple_plot("Creating plot with total cases...", "/world_total cases.png", 2, "Nombre total de cas", output_folder, world_dictionnary)
	else:
		print("Please specify the output")

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
@click.option("-a", 
	"--total_deaths", 
	is_flag=True,
	help="Process the cumulative deaths")
@click.option("-b", 
	"--cases_of_the_day", 
	is_flag=True,
	help="Process the cases of the day")
@click.option("-d", 
	"--deaths_of_the_day", 
	is_flag=True,
	help="Process the deaths of the day")
@click.option("-e", 
	"--total_cases", 
	is_flag=True,
	help="Process the cumulative cases")
def country(country, output_folder, full, liste, total_deaths, total_cases, cases_of_the_day, deaths_of_the_day):
	"""
	Create a CSV file with today's data for today's deaths, total deaths, today's cases, total cases for the country(ies) given in parameter.
	If -a, -b, -d or -e are not precised, they are all process.

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
	:return: create CSV files
	:rtype: None
	"""
	start_time = time.time()

	# managing the folders...
	os.system('mkdir ' + output_folder)	

	if total_deaths:
		csv_path = output_folder + '/total_deaths.csv'
		with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print('Writing headers...')
				writer.writerow(["country", "total_deaths"])
				for country in get_list_countries_to_process(country=country, full=full, liste=liste):
					print(country + ' on process...')
					if country in get_data_today(DATA_PATH):
						writer.writerow([country, get_data_today(DATA_PATH)[country][3]])
	elif total_cases:
		csv_path = output_folder + '/total_cases.csv'
		with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print('Writing headers...')
				writer.writerow(["country", "total_cases"])
				for country in get_list_countries_to_process(country=country, full=full, liste=liste):
					print(country + ' on process...')
					if country in get_data_today(DATA_PATH):
						writer.writerow([country, get_data_today(DATA_PATH)[country][2]])
	elif cases_of_the_day:
		csv_path = output_folder + '/cases_of_the_day.csv'
		with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print('Writing headers...')
				writer.writerow(["country", "cases_of_the_day"])
				for country in get_list_countries_to_process(country=country, full=full, liste=liste):
					print(country + ' on process...')
					if country in get_data_today(DATA_PATH):
						writer.writerow([country, get_data_today(DATA_PATH)[country][0]])
	elif deaths_of_the_day:
		csv_path = output_folder + '/deaths_of_the_day.csv'
		with open(csv_path, 'w') as f:
				writer = csv.writer(f)
				print('Writing headers...')
				writer.writerow(["country", "deaths_of_the_day"])
				for country in get_list_countries_to_process(country=country, full=full, liste=liste):
					print(country + ' on process...')
					if country in get_data_today(DATA_PATH):
						writer.writerow([country, get_data_today(DATA_PATH)[country][1]])
	else: # create a CSV with all the data (total_deaths, total_cases, cases_of_the_day, deaths_of_the_day)
		csv_path = output_folder + '/deaths_of_the_day.csv'
		with open(csv_path, 'w') as f:
			writer = csv.writer(f)
			print('Writing headers...')
			writer.writerow(["country", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths"])
			for country in get_list_countries_to_process(country=country, full=full, liste=liste):
				print(country + ' on process...')
				if country in get_data_today(DATA_PATH):
					writer.writerow([country, get_data_today(DATA_PATH)[country][0], get_data_today(DATA_PATH)[country][1], get_data_today(DATA_PATH)[country][2], get_data_today(DATA_PATH)[country][3]])

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
	:return: create CSV files
	:rtype: None
	"""
	start_time = time.time()

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
				writer.writerow(["date", "country", "cases_of_the_day", "deaths_of_the_day", "total_cases", "total_deaths"])
				print("Writing body...")
				for line in f_o:
					# écriture des lignes que quand le nombre de cas est supérieur à PLOT_MIN_CASES
					if line[1] == country and line[4] >= PLOT_MIN_CASES:
						writer.writerow(line)

	print("Execution time : %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()