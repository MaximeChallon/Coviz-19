import click
from utilitaires.fonctions import *
import os
import time
import csv
from utilitaires.constantes import *

clean_folder()

DATA = os.system('wget https://covid.ourworldindata.org/data/ecdc/full_data.csv')
DATA_PATH = 'full_data.csv'

@click.group()
def main():
    pass

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