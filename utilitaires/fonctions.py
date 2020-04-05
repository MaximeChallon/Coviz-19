import os
import csv

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
		# passage de l'en-tête
		next(f_o)
		# création de la liste des pays concernés
		list_countries = []
		for line in f_o:
			if line[1] not in list_countries:
				list_countries.append(line[1])
		return list_countries