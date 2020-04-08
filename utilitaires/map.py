from utilitaires.fonctions import *
import os
import csv
from utilitaires.constantes import *
import folium
import pandas as pd
import re

def map_chloro(index_layer, index_plot, min_plot, output_folder):
    print('Loading capitals data...')
    # open the json file with the json data of capitals
    capitals_json = open('utilitaires/data/data_capitals.geojson')
    capitals = json.load(capitals_json)
    
    print("Loading countries data...")
    # open the json file with dates of quarantine
    country_json = open('utilitaires/data/data_countries.geojson')
    pays = json.load(country_json)

    # gestion des titres pour la couche des pays
    if index_layer == 2:
        titre_layer = "Nouveaux cas recensés dans la journée d hier"
    elif index_layer == 3:
        titre_layer = "Nouveaux décès recensés dans la journée d hier"
    elif index_layer == 4:
        titre_layer = "Nombre de cas total recensés"
    elif index_layer == 5:
        titre_layer = "Nombre de décès total recensés"

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
    
    
    print("Processing your given dataset...")
    with open(DATA_PATH, 'r') as f:
    	f_o = csv.reader(f)
    	next(f_o)
    	with open('data.csv', "w") as f_csv:
    		writer = csv.writer(f_csv)
    		writer.writerow(["Country", "Chiffre"])
    		for line in f_o:
          # data.csv prend en valeur la date de la veille avec le nombre de décès total, hors World: ça
          # permet de faire le fonds de carte de couleur en fonction du dernier chiffre du nombre de décès
    			if line[0] == str(YESTERDAY_CUT) and line[1] != 'World':
    				writer.writerow([line[1], line[index_layer]])
    
    countries_geo = f'utilitaires/data/data_countries.geojson'
    data = f'data.csv'
    world_data = pd.read_csv(data)
    
    print("Creating the countries's layer of the map...")
    map = folium.Map(location=[48, 0], zoom_start=3)
    
    # création du fonds de carte coloré en fonction des valeurs de la veille
    folium.Choropleth(
        geo_data=countries_geo,
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
        data_country = []
        # création d'un booléen pour savoir si le pays aura un graphique
        data_plot = False
        with open(DATA_PATH, 'r') as f_e:
            f_o = csv.reader(f_e)
            next(f_o)
            i = 1
            for line in f_o:
                if pays['properties']['country'] == line[1] and int(line[index_plot]) >= min_plot:
                    dico = {
    					"col": "Nombre",
    					"idx": i,
    					"val": int(line[index_plot])
    				}
                    data_country.append(dico)
                    i += 1
                    data_plot = True
    
    	# créer le fichier json
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
                f.write(json.dumps(data))

            with open('country.json', 'r') as f:
                data_json = json.load(f)

            custom_icon = folium.features.CustomIcon(icon_image='utilitaires/coro.png', icon_size=(14, 14))

            folium.Marker(location=pays['geometry']['coordinates'],
                          popup=folium.Popup(max_width=900).add_child(
                              folium.Vega(data_json, width=900, height=450)),
                            icon=custom_icon
                      	).add_to(map)

            os.remove('country.json')

    print("Creating the HTML file...")
    folium.LayerControl().add_to(map)

    os.mkdir(output_folder)
    map.save(output_folder + '/index.html')

    country_json.close()
    capitals_json.close()

    os.remove('data.csv')   