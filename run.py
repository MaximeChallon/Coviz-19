import click
from utilitaires.fonctions import clean_folder, get_list_countries
import os
import time
from datetime import datetime
import csv

TODAY = datetime.today().strftime('%Y-%m-%d')

clean_folder()

DATA = os.system('wget https://covid.ourworldindata.org/data/ecdc/full_data.csv')
DATA_PATH = 'full_data.csv'
GRAPH_MIN_CASES = '100'

@click.group()
def main():
    pass

@main.command("country")
@click.argument("output_folder",
              default="out")
@click.option("-c", 
	'--country' ,
	help='Execute the command for the country')
@click.option("-f", 
	"--full", 
	default=False, 
	help="Execute the command for all the countries")
@click.option("-l", 
	"--liste", 
	default=[],
	help="Execute the command for a list of countries")
def country(country, output_folder, full, list):
	start_time = time.time()
	print()
	print("Execution time : %s seconds ---" % (time.time() - start_time))




@main.command("csv")
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
	start_time = time.time()

	# list of countries to process
	list_countries_to_process = []
	if country in get_list_countries(DATA_PATH):
		list_countries_to_process.append(country)
	elif full:
		list_countries_to_process = get_list_countries(DATA_PATH)
	elif liste :
		liste = liste[1:-1]
		countries = liste.split(',')
		for one_country in countries:
			if one_country in get_list_countries(DATA_PATH):
				list_countries_to_process.append(one_country)
			else:
				print(one_country + ' not found in the available countries list.')
	else:
		print("Country not found, please check the available countries in the following list.")
		print(get_list_countries(DATA_PATH))

	# managing the folders...
	folder_path = output_folder + '/countries'
	os.makedirs(folder_path)

	for country in list_countries_to_process:
		print(country + ' processing...')
		# creation of one folder for each country
		csv_path = folder_path + '/' + country + '.csv'

		with open(DATA_PATH, 'r') as f:
			f_o = csv.reader(f)
			next(f_o)
			for line in f_o:
				# écriture des lignes que quand le nombre de cas est supérieur à CAS_MIN_GRAPHIQUE
				if line[1] == country and line[4] >= GRAPH_MIN_CASES:
					with open(csv_path, 'a') as f_e:
						writer = csv.writer(f_e)
						writer.writerow(line)

	print("Execution time : %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()