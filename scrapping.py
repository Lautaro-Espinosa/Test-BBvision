import json
import requests
import csv

if __name__ == '__main__':
    #pelis
    url_scrap = 'https://playdata.starz.com/metadata-service/play/partner/Web_AR/v8/content?lang=es-419&contentType=Movie'

    request_url = requests.get(url_scrap)

    json_pelis = request_url.json()

    playContentArray = json_pelis['playContentArray']
    peliculas = playContentArray['playContents']

    with open('peliculas_start.json','w') as f:
        json.dump(playContentArray, f, indent=4)

    t = open('peliculas_start.json',)

    json_cargas = json.load(t)

    sub_meta_data = []
    #["titulo","duracion", "año de estreno", "descripcion" , "link"]
    meta_data = []
    link = ""
    for json_cargas in peliculas:
        sub_meta_data.append(json_cargas.get('title'))
        sub_meta_data.append(json_cargas.get('runtime'))
        sub_meta_data.append(json_cargas.get('releaseYear'))
        sub_meta_data.append(json_cargas.get('logLine'))
        #cambiamos los espacios por - del titulo y le sumamos el Id para obtener la peli
        link = str(json_cargas.get('title')) + '-' + str(json_cargas.get('contentId'))
        link = link.replace(" ", "-")
        link = "https://www.starz.com/ar/es/movies/" + link
        sub_meta_data.append(link)
        meta_data.append(sub_meta_data)
        sub_meta_data = []

    #los escribimos en CSV para poder pasarlo a  la base de datos.
    with open ('metadate_pelis.csv','w', newline = '') as file:
       writer = csv.writer(file, delimiter=';')
       try:
           writer.writerows(meta_data)
       except:
            print("error en el encode1")

    #Series
    url_scrap = 'https://playdata.starz.com/metadata-service/play/partner/Web_AR/v8/content?lang=es-419&contentType=Series%20with%20Season'

    request_url = requests.get(url_scrap)

    json_series = request_url.json()

    playContentArray = json_series['playContentArray']
    series = playContentArray['playContents']

    with open('series_start.json','w') as r:
        json.dump(playContentArray, r, indent=4)

    s = open('series_start.json',)

    json_cargas_series = json.load(s)
    meta_data1 = []
    link = ""
    for json_cargas_series in series:
        try:
            sub_meta_data.append(json_cargas_series.get('title'))
            sub_meta_data.append(json_cargas_series.get('minReleaseYear'))
            sub_meta_data.append(json_cargas_series.get('logLine'))
            link = str(json_cargas_series.get('title')) + '-' + str(json_cargas_series.get('contentId')) 
            link = link.replace(" ", "-")
            link = "https://www.starz.com/ar/es/series/" + link
            sub_meta_data.append(link)
            meta_data1.append(sub_meta_data)
            sub_meta_data = []
        except:
            print("error en el encode2")

    with open ('metadate_series.csv','w',newline = '') as fileSeries:
       writerSeries = csv.writer(fileSeries, delimiter=';')
       writerSeries.writerows(meta_data1)
