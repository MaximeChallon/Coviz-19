from utilitaires.fonctions import *
import os
import time
import csv
from utilitaires.constantes import *
import folium
import pandas as pd
import re
import requests

def map_chloro():
    # open the json file with the json data of capitals
    capitals_json = open('utilitaires/data/data_capitals.geojson')
    capitals = json.load(capitals_json)
    
    # open the json file with dates of quarantine
    country_json = open('utilitaires/data/data_countries.geojson')
    pays = json.load(country_json)
    
    
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
    				writer.writerow([line[1], line[5]])
    
    countries_geo = f'utilitaires/data/data_countries.geojson'
    data = f'data.csv'
    world_data = pd.read_csv(data)
    
    map = folium.Map(location=[48, -102], zoom_start=3)
    
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
        legend_name='Nombre de décès total'
    	).add_to(map)
    
    
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
                if pays['properties']['country'] == line[1] and int(line[5]) >= 5:
                    dico = {
    					"col": "Nombre",
    					"idx": i,
    					"val": int(line[5])
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
                        "title": "Jours depuis le 5ème décès enregistré",
                        "type": "x"
                      },
                      {
                        "scale": "y",
                        "title": "Nombre de décès total",
                        "type": "y"
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

    folium.LayerControl().add_to(map)

    os.mkdir('out')
    map.save('out/index.html')

    country_json.close()
    capitals_json.close()

    os.remove('data.csv')   