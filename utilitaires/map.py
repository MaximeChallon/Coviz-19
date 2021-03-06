from utilitaires.fonctions import *
import os
import csv
from utilitaires.constantes import *
import folium
import pandas as pd
import re

def map_chloro(index_layer, index_plot, min_plot, output_folder):
    """
    Create a Leaflet chloropeth map with Folium and Vega libraries. Each country has his own plot for the given data.
    :param index_layer: index of the data in the DATA_PATH csv
    :type index_layer: int
    :param index_plot: index of the data in the DATA_PATH csv
    :type index_plot: int
    :param min_plot: the minimal value of y axes for which the data will be process
    :type min_plot: float
    :param output_folder: name of the folder where to save the map
    :type output_folder: str
    :return: nothing
    :rtype: None
    """
    print('Loading capitals data...')

    # open the json file with the json data of capitals
    capitals_json = open('utilitaires/data/data_capitals.geojson')
    capitals = json.load(capitals_json)
    
    print("Loading countries data...")

    # open the json file with dates of quarantine
    country_json = open('utilitaires/data/data_country.geojson')
    pays = json.load(country_json)

    # gestion des titres pour la couche des pays
    if index_layer == 2:
        titre_layer = "Nouveaux cas recensés dans la journée d hier"
        titre_fichier = "nouveaux_cas"
    elif index_layer == 3:
        titre_layer = "Nouveaux décès recensés dans la journée d hier"
        titre_fichier = "nouveaux_deces"
    elif index_layer == 4:
        titre_layer = "Nombre de cas total recensés"
        titre_fichier = "cas_total"
    elif index_layer == 5:
        titre_layer = "Nombre de décès total recensés"
        titre_fichier = "deces_total"
    elif index_layer == 6:
        titre_layer = "Nombre de cas recensés la veillepour 10000 habitants"
        titre_fichier = "nouveaux_cas_10000"
    elif index_layer == 7:
        titre_layer = "Nombre de décès recensés la veille pour 10000 habitants"
        titre_fichier = "nouveaux_deces_10000"
    elif index_layer == 8:
        titre_layer = "Nombre total de cas pour 10000 habitants"
        titre_fichier = "cas_total_10000"
    elif index_layer == 9:
        titre_layer = "Nombre total de décès pour 10000 habitants"
        titre_fichier = "deces_total_10000"

    # gestion des titres pour les graphiques
    if index_plot == 2:
        x_plot = "Jours depuis le premier jour ayant " + str(min_plot) + " nouveaux cas recensés la veille"
        y_plot = "Nombre de nouveaux cas recensés la veille"
    elif index_plot == 3:
        x_plot = "Jours depuis le premier jour ayant " + str(min_plot) + " nouveaux décès recensés la veille"
        y_plot = "Nombre de nouveaux décès recensés la veille"
    elif index_plot == 4:
        x_plot = "Jours depuis un total de " + str(min_plot) + "  cas"
        y_plot = "Nombre de cas recensés "
    elif index_plot == 5:
        x_plot = "Jours depuis un total de " + str(min_plot) + "  décès"
        y_plot = "Nombre de décès recensés "
    elif index_plot == 6:
        x_plot = "Jours depuis le premier jour ayant " + str(min_plot) + " nouveaux cas recensés la veille pour 10000 habitants"
        y_plot = "Nombre de nouveaux cas recensés la veille pour 10000 habitants"
    elif index_plot == 7:
        x_plot = "Jours depuis le premier jour ayant " + str(min_plot) + " nouveaux décès recensés la veille pour 10000 habitants"
        y_plot = "Nombre de nouveaux décès recensés la veille pour 10000 habitants"
    elif index_plot == 8:
        x_plot = "Jours depuis un total de " + str(min_plot) + "  cas pour 10000 habitants"
        y_plot = "Nombre de cas recensés pour 10000 habitants"
    elif index_plot == 9:
        x_plot = "Jours depuis un total de " + str(min_plot) + "  décès pour 10000 habitants"
        y_plot = "Nombre de décès recensés pour 10000 habitants"
    
    
    print("Processing your given dataset...")

    # création d'un fichier csv temporaire contenant les données pour la carte selon l'index_layer
    with open(DATA_PATH, 'r') as f:
    	f_o = csv.reader(f)
    	next(f_o)
    	with open('data.csv', "w") as f_csv:
    		writer = csv.writer(f_csv)
    		writer.writerow(["Country", "Chiffre"])
    		for line in f_o:
          # data.csv prend en valeur la date de la veille avec le nombre correspondant, hors World
    			if line[0] == str(YESTERDAY_CUT) and line[1] != 'World':
    				writer.writerow([line[1], line[index_layer]])
    
    # ouverture et lecture du fichier csv créé
    data = f'data.csv'
    world_data = pd.read_csv(data)
    
    print("Creating the countries's layer of the map...")

    # initialisation de la carte et des paramètres généraux
    map = folium.Map(location=[48, 0], zoom_start=3)
    
    # création du fonds de carte coloré en fonction des valeurs de la veille
    folium.Choropleth(
        geo_data=pays,
        name='choropleth',
        data=world_data,
        columns=['Country', 'Chiffre'],
        key_on='feature.id',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=titre_layer
    	).add_to(map)
    
    
    print("Processing plots for each country...")

    # création d'un point par pays (sur la capitale) pour accueillir les graphiques ensuite
    for pays in capitals["features"]:
        # création d'une liste vide qui accueillera un dictionnaire par jour pour le pays donné
        data_country = []
        # création d'un booléen pour savoir si le pays aura un graphique
        data_plot = False
        with open(DATA_PATH, 'r') as f_e:
            f_o = csv.reader(f_e)
            next(f_o)
            # la variable i permet non pas d'afficher le jour précis sur l'axe x, mais le numéro du jour en fonction
            # de la réalisation du paramètre min_plot
            i = 1
            for line in f_o:
                if pays['properties']['country'] == line[1] and float(line[index_plot]) >= float(min_plot):
                    dico = {
    					"col": "Nombre",
    					"idx": i,
    					"val": float(line[index_plot])
    				}
                    data_country.append(dico)
                    i += 1
                    data_plot = True
    
    	# créer le fichier json nécessaire à Vega pour faire les graphiques
        if data_plot:
            with open('country.json', "w") as f:
                data = {
                    "axes": [
                      {
                        "scale": "x",
                        "title": x_plot,
                        "type": "x"
                      },
                      {
                        "scale": "y",
                        "title": y_plot,
                        "type": "y",
                        "grid": True
                      }
                    ],
                    "data": [
                      {
                        "name": "table",
                        "values": data_country
                      }
                    ],
                    "height": 400,
                    "legends": [],
                    "marks": [
                      {
                        "from": {
                          "data": "table",
                          "transform": [
                            {
                              "keys": [
                                "data.col"
                              ],
                              "type": "facet"
                            }
                          ]
                        },
                        "marks": [
                          {
                            "properties": {
                              "enter": {
                                "stroke": {
                                  "field": "data.col",
                                  "scale": "color"
                                },
                                "strokeWidth": {
                                  "value": 2
                                },
                                "x": {
                                  "field": "data.idx",
                                  "scale": "x"
                                },
                                "y": {
                                  "field": "data.val",
                                  "scale": "y"
                                }
                              }
                            },
                            "type": "line"
                          }
                        ],
                        "type": "group"
                      }
                    ],
                    "padding": "auto",
                    "scales": [
                      {
                        "domain": {
                          "data": "table",
                          "field": "data.idx"
                        },
                        "name": "x",
                        "range": "width",
                        "nice": True
                      },
                      {
                        "domain": {
                          "data": "table",
                          "field": "data.val"
                        },
                        "name": "y",
                        "nice": True,
                        "range": "height"
                      },
                      {
                        "domain": {
                          "data": "table",
                          "field": "data.col"
                        },
                        "name": "color",
                        "range": "category20",
                        "type": "ordinal"
                      }
                    ],
                    "width": 800
                  }
                # écriture du dictionnaire dans un fichier json
                f.write(json.dumps(data))

            # ouverture et lecture de ce nouveau fichier json...
            with open('country.json', 'r') as f:
                data_json = json.load(f)

            custom_icon = folium.features.CustomIcon(icon_image='utilitaires/img/coro.png', icon_size=(14, 14))

            # ... pour le donner à folium.Vega dans le marker placé sur la capitale de chaque pays
            folium.Marker(location=pays['geometry']['coordinates'],
                          popup=folium.Popup(max_width=900).add_child(
                              folium.Vega(data_json, width=900, height=450)),
                            icon=custom_icon
                      	).add_to(map)

            os.remove('country.json')

    print("Creating the HTML file...")
    
    folium.LayerControl().add_to(map)

    os.mkdir(output_folder)
    map.save(output_folder + '/map_' + titre_fichier + '.html')

    country_json.close()
    capitals_json.close()

    os.remove('data.csv')   