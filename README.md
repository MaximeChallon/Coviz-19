# Lancement

`python3 run.py [COMMANDE] [OPTIONS] [OUTPUT_FOLDER]`

`python3 run.py --help` pour voir les commandes disponibles.

# Commandes

## `csv_country`

`csv_country` permet de générer des fichiers CSV pour un plusieurs pays avec les informations suivantes:

* date 
* country
* cases_of_the_day
* deaths_of_the_day
* total_cases
* total_deaths

Pour spécifier le(s) pays dont on souhaite les données depuis le 31 décembre 2019, utiliser les options suivantes:

* `-c`, `--country` : Execute the command for the country
* `-f`, `--full` : Execute the command for all the countries
* `-l`, `--liste` : Execute the command for a list of countries
* `-h`, `--help` : Show this message and exit.


## `today`

`today` permet de créer un fichier CSV pour les données du jour-même selon les pays spécifiés et les données voulues. Si les données datent de la veille (car pas encore mises à jour sur le site soucre), un message s'affichera, et ces données de la veille seront utilisées. De nombreuses options sont disponibles et sont à combiner:

* `-c`, `--country` : Execute the command for the country
* `-f`, `--full` : Execute the command for all the countries
* `-l`, `--liste` : Execute the command for a list of countries
* `-a`, `--total_deaths` : Process the cumulative deaths
* `-b`, `--cases_of_the_day` : Process the cases of the day
* `-d`, `--deaths_of_the_day` : Process the deaths of the day
* `-e`, `--total_cases` : Process the cumulative cases
* `-h`, `--help` : Show this message and exit.

Voici un tableau récapitulatif des résultats qu'il est possible d'obtenir (données d'exemple):

|Options|`-c`|`-f`|`-l`|
|:-:|:-:|:-:|:-:|
|`-a`|country,total_deaths</br>France,7560|country,total_deaths</br>France,7560</br>Italy,15362</br>...|country,total_deaths</br>France,7560</br>Italy,15362|
|`-b`|country,cases_of_the_day</br>France,4267|country,cases_of_the_day</br>France,4267</br>Italy,4805</br>...|country,cases_of_the_day</br>France,4267</br>Italy,4805|
|`-d`|country,deaths_of_the_day</br>France,1053|country,deaths_of_the_day</br>France,1053</br>Italy,681</br>...|country,deaths_of_the_day</br>France,1053</br>Italy,681|
|`-e`|country,total_cases</br>France,68605|country,total_cases</br>France,68605</br>Italy,124632</br>...|country,total_cases</br>France,68605</br>Italy,124632|
|`-a`, `-b`, </br> `-d` ou `-e`</br> non spécifiés|country,cases_of_the_day,deaths_of_the_day,total_cases,total_deaths</br>France,4267,1053,68605,7560|country,cases_of_the_day,deaths_of_the_day,total_cases,total_deaths</br>France,4267,1053,68605,7560</br>Italy,4805,681,124632,15362</br>...|country,cases_of_the_day,deaths_of_the_day,total_cases,total_deaths</br>France,4267,1053,68605,7560</br>Italy,4805,681,124632,15362|

## `world`

`world` permet de traiter uniquement les données globales mondiales et d'obtenir des CSV et des graphiques selon la date souhaitée (celle du jour-même, ou jour par jour depuis le 31 décembre 2019).

De nombreuses options sont disponibles:

* `-t`, `--today`  : Process the data of today
* `-f`, `--full`: Process all the data from all the dates available
* `-cf`, `--csv_full` : Create a CSV file as output with all data
* `-cdd`, `--csv_deaths_of_the_day` : Create a CSV file as output with the deaths of the day
* `-ctd`, `--csv_total_deaths` : Create a CSV file as output with the cumulative deaths
* `-ctc`, `--csv_total_cases` : Create a CSV file as output with the cumulative cases
* `-ccd`, `--csv_cases_of_the_day` : Create a CSV file as output with the cases of the day
* `-pf`, `--plot_full` : 
* `-h`, `--help` : Show this message and exit.

Voici un tableau récapitulatif des résultats qu'il est possible d'obtenir (données d'exemple):

|Options|`-t`|`-f`|
|:-:|:-:|:-:|
|`-cf`|date_today, cases_of_the_day, deaths_of_the_day, total_cases, total_deaths </br> 2020-04-06, 10000, 5000, 100000, 50000|for_each_date, cases_of_the_day, deaths_of_the_day, total_cases, total_deaths </br> 2019-12-31, 0, 0, 0, 0 </br> ... </br> 2020-04-05, 9000, 4000, 90000, 40000 </br> 2020-04-06, 10000, 5000, 100000, 50000|
|`-cdd`|date_today, deaths_of_the_day </br> 2020-04-06, 5000|for_each_date, deaths_of_the_day </br> 2019-12-31, 0 </br> ... </br> 2020-04-05, 4000</br> 2020-04-06, 5000|
|`-ctd`|date_today, total_deaths </br> 2020-04-06, 50000|for_each_date, total_deaths </br> 2020-12-31, 0 </br> ... </br> 2020-04-05, 40000 </br> 2020-04-06, 50000|
|`-ctc`|date_today, total_cases </br> 2020-04-06, 100000|for_each_date, total_cases </br> 2020-12-31, 0 </br> ... </br> 2020-04-05, 90000 </br> 2020-04-06, 100000|
|`-ccd`|date_today, cases_of_the_day </br> 2020-04-06, 10000|for_each_date, cases_of_the_day </br> 2020-12-31, 0 </br> ... </br> 2020-04-05, 9000 </br> 2020-04-06, 10000|