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
def country(country, output_folder, full, liste):
	start_time = time.time()
	
	print(get_data_today(DATA_PATH))

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

	# managing the folders...
	folder_path = output_folder + '/countries'
	os.system('mkdir ' + output_folder)
	os.system('mkdir ' + output_folder + '/countries')

	for country in get_list_countries_to_process(country=country, full=full, liste=liste):
		print(country + ' processing...')
		# creation of one folder for each country
		os.system('mkdir ' + folder_path + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_'))
		csv_path = folder_path + '/' + country.replace(' ', '_').replace('\'', '_').replace('(', '_').replace(')', '_') + '/' +  country.replace(')', '_').replace('(', '_').replace(' ', '_').replace('\'', '_') + '.csv'

		with open(DATA_PATH, 'r') as f:
			f_o = csv.reader(f)
			next(f_o)
			for line in f_o:
				# écriture des lignes que quand le nombre de cas est supérieur à CAS_MIN_GRAPHIQUE
				if line[1] == country and line[4] >= PLOT_MIN_CASES:
					with open(csv_path, 'a') as f_e:
						writer = csv.writer(f_e)
						writer.writerow(line)

	print("Execution time : %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()