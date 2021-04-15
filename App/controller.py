"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import datetime as dt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de vídeos



def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.

    Retorna el catálogo.
    """
    catalog = model.newCatalog()
    return catalog



# Funciones para la carga de datos



def loadData(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadCategoryID(catalog)
    video1, size = loadVideos(catalog)
    return video1, size



def loadCategoryID(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga las categorías del archivo.
    """
    categoryfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'), delimiter="\t")
    for category in input_file:
        filtered_category = {
            'id': category['id'],
            'name': (category['name']).replace(" ", '')  # quitar los espacios
        }

        model.addCategoryID(catalog, filtered_category)




def loadVideos(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga todos los vídeos del archivo y los agrega a la lista de vídeos
    """
    videosfile = cf.data_dir + 'videos/videos-large.csv'  # videos-large para la entrega
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))

    video1 = None
    size = 0
    for video in input_file:

        filtered_video = {
            'video_id': video['video_id'],
            'trending_date': dt.datetime.strptime(video['trending_date'], '%y.%d.%m').date(),
            'title': video['title'],
            'channel_title': video['channel_title'],
            'category_id': int(video['category_id']),
            'publish_time': dt.datetime.strptime(video['publish_time'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'tags': video['tags'].replace("\"", ''),
            'views': int(video['views']),
            'likes': int(video['likes']),
            'dislikes': int(video['dislikes']),
            'country': video['country'],
            'dias_t': 1
        }

        if size == 0:
            video1 = filtered_video

        size += 1
        model.addVideoCountry(catalog, filtered_video['country'], filtered_video)
        model.addVideoCategory(catalog, filtered_video['category_id'], filtered_video)

    return video1, size



# Funciones de ordenamiento



def sortVideos(catalog, cmp: int):
    """
    Args:
        catalog: Catálogo de videos.
        cmp: (1) cmpVideosByViews (2) cmpVideosByTitle (3) cmpVideosByLikes

    Return:
        list: Ordena los vídeos según sus views.
    """

    return model.sortVideos(catalog, cmp)



# Funciones de consulta sobre el catálogo



def primerVideo(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Return:
        video1: Retorna el primero video cargado en el catálogo.
    """
    video1 = model.primerVideo(catalog)
    return video1




def getVideosByCategoryOrCountry(catalog, categoryName, countryName, categoryCatalog):
    """
    Args:
        catalog: Catálogo de videos.
        categoryName: Nombre de la categoría para flitrar los videos.
        countryName: Nombre del país.

    Return:
        list: catálogo filtrado por el nombre de la categoría y el país ingresado por parámetro.
    """

    category = model.getVideosByCategoryOrCountry(catalog, categoryName, countryName, categoryCatalog)

    return category




def getVideosByTag(catalog, tag: str):
    """
    Args:
        catalog: Catálogo de videos
        tag: Nombre del tag ingresado por el usuario
        countryName: Nombre del país.

    Return:
        tag: Catálogo filtrado de acuerdo con el tag y el país ingresado por parámetro
    """
    tag = model.getVideosByTag(catalog, tag)
    return tag



def getVideosByTagTwo(catalog, tag: str):
    """
    Args:
        catalog: Catálogo de videos
        tag: Nombre del tag ingresado por el usuario
        countryName: Nombre del país.

    Return:
        tag: Catálogo filtrado de acuerdo con el tag y el país ingresado por parámetro
    """

    return model.getVideosByTagTwo(catalog, tag)



def getMap(catalog, name):
    """
    Args:
        catalog: Catálogo con todos los videos.
        name: Nombre del país o la categoría con la que se desea crear el mapa.

    Return:
        filtered_catalog: resultado de la función mp.get()
    """
    filtered_catalog = model.getMap(catalog, name)
    return filtered_catalog



def filtroPaisCategoria(catalog, country, category):

    return model.filtroPaisCategoria(catalog, country, category)



# Funciones de operaciones sobre el catálogo



def masDiasTrending(catalog, llave: int):
    """
    Args:
        catalog: Catálogo ordenado según los Títulos
        llave: (1) 'title' o (2) 'video_id'

    Return:
        video_mayor_dias: Video que ha tenido más días de tendencia.
    """
    catalog = model.masDiasTrending(catalog, llave)
    return catalog
