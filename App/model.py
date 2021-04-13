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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
"""

import datetime  # Se importa para que al imprimir información de los vídeos aparezca como una fecha legible.
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort
assert cf


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las
categorias de los mismos.
"""


# Construccion de modelos



def newCatalog():
    """
    Inicializa el catálogo de videos. Crea una lista vacía para guardar.
    todos los videos. Adicionalmente, crea una lista vacía para las categorías.

    Retorna el catálogo inicializado.
    """

    catalog = {'videos': None, 'category_id': None, 'country': None, 'categories': None}

    # Se crean las listas bajo esas llaves
    catalog['videos'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpVideosByViews)

    catalog['category_id'] = mp.newMap(numelements=30, prime=31, maptype="PROBING", loadfactor=0.9, comparefunction=cmpCategoriasByName)  # Cambios del laboratorio 6.

    catalog['country'] = mp.newMap(numelements=10, prime=11, maptype="PROBING", loadfactor=0.9, comparefunction=cmpByCountry)

    return catalog



# Funciones para agregar informacion al catalogo



def addVideo(catalog, video):
    """
    Args:
        catalog: Catálogo de videos.
        video: Video que desea agregarse en el catálogo.

    Adiciona un video a la lista de videos.
    """

    # Se adiciona el vidieo en la última posición de la lista de videos.
    lt.addLast(catalog['videos'], video)




def addCategoryID(catalog, category):
    """
    Args:
        catalog: Catálogo de videos.
        category: Nombre de la categoría que desea agregarse en el catálogo.

    Adiciona una categoría a la lista de categorías.
    """
    # Se crea la nueva categoría. Cambios laboratorio 6:
    newCat = newCategoryID(category['name'], category['id'])
    mp.put(catalog['category_id'], category['name'].lower(), newCat)




def addVideoCategory(catalog, category_id, video):
    mapa = catalog['category_id']

    categoryName = categoryIDtoName(catalog, category_id)[1]

    if (categoryName is not None) and not mp.contains(mapa, categoryName):

        nuevoCategory = newCategoryID(categoryName.lower(), category_id)
        mp.put(mapa, categoryName, nuevoCategory)

    elif (categoryName is not None) and mp.contains(mapa, categoryName):
        nuevoCategory = mp.get(mapa, categoryName)['value']
    

    if categoryName is not None:
        lt.addLast(nuevoCategory['videos'], video)




def addVideoCountry(catalog, countryName, video):
    """
    Args:
        catalog: Catálogo de videos.
        countryName: Nombre del país con el que se desea filtrar el catálogo.
        video: video que desea agregarse en caso de que no exista.

    Filtra el carálogo de vídeos por país.
    """
    mapa = catalog['country']

    if not mp.contains(mapa, countryName):

        nuevoCountry = newCountry(countryName.lower())
        mp.put(mapa, countryName, nuevoCountry)

    else:
        nuevoCountry = mp.get(mapa, countryName)['value']
    

    lt.addLast(nuevoCountry['videos'], video)



# Funciones para creacion de datos



def newCategoryID(name, id_):
    """
    Args:
        name: Nombre de la categoría.
        id: Número asignado a esa categoría que entra por parámetro.

    Esta estructura almacena las categorías utilizadas para marcar videos.
    """

    category = {'name': '', 'category_id': '', 'videos': None}

    category['name'] = name.lower()
    category['category_id'] = int(id_)
    category['videos'] = lt.newList('ARRAY_LIST', cmpfunction=cmpVideosByViews)


    return category




def newCountry(countryName):
    """
    Args:
        countryName: Nombre del país.

    Esta estructura almacena el país que entra por parámetro para marcar videos.
    """
    country = {'name': '', 'videos': None}
    country['name'] = countryName.lower()
    country['videos'] = lt.newList('ARRAY_LIST', cmpfunction=cmpVideosByViews)
    return country



# Funciones de consulta



def primerVideo(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Retorna el primer video cargado.
    """
    video1 = lt.getElement(catalog["videos"], 1)
    return video1




def getVideosByCountry(catalog, countryName: str):
    """
    Args:
        catalog: Catálogo de videos.
        countryName: Nombre del país.

    Filtra el catálogo de acuerdo a los parámetros indicados.
    """
    posCountry = lt.isPresent(catalog['country'], countryName)  # recibo la posición del país en el catálogo
    if posCountry > 0:
        country = lt.getElement(catalog['country'], posCountry)  # recibe el array del país que contiene el name y videos
        return country
    return None




def getVideosByTagCountry(catalog, tag: str):
    """
    Args:
        catalog: Catálogo de videos.
        tag: Nombre del tag.
        country: Nombre del país.

    Filtra el catálogo de acuerdo a los parámetros indicados.
    """
    #TODO: Ver si toca usar mapa
    catalogo_filtrado = {'tag': tag, 'videos': None}
    catalogo_filtrado['videos'] = lt.newList('ARRAY_LIST', cmpfunction=cmpVideosByLikes)

    for video in lt.iterator(catalog['videos']):

        if tag.lower() in video['tags'].lower():

            lt.addLast(catalogo_filtrado['videos'], video)

    return catalogo_filtrado




def getVideosByCategoryOrCountry(catalog, categoryName: str, country, categoryCatalog):
    """
    Args:
        catalog: Catálogo del país
        categoryName: Nombre del país
        country: Nombre del país

    Return:
        list: Catálogo filtrado de acuerdo a los parámetros.
    """

    id_, name = categoryNameToID(categoryCatalog, categoryName)  # del catálogo principal, cambia categoryName por su id

    catalogo_filtrado = {'name': name, 'videos': None}
    catalogo_filtrado['videos'] = lt.newList('ARRAY_LIST', cmpfunction=cmpVideosByViews)


    for video in lt.iterator(catalog['videos']):  # Ciclo para iterar por cada video del catálogo

        if video['category_id'] == id_ and (country is not None) and video['country'].lower() == country.lower():

            lt.addLast(catalogo_filtrado['videos'], video)  # se agrega al catálogo filtrado

        elif video['category_id'] == id_ and country is None:

            lt.addLast(catalogo_filtrado['videos'], video)

    return catalogo_filtrado




def masDiasTrending(ord_videos, llave=2):
    """
    Args:
        catalog: Catálogo ordenado según los Títulos
        llave: (1) 'title' o (2) 'video_id'

    Return:
        video_con_mas_dias: Video que ha tenido más días de tendencia.
    """
    if llave == 1:
        llave = 'title'
    else:
        llave = 'video_id'

    size = lt.size(ord_videos)

    video_con_mas_dias = None
    mas_dias = 1

    i = 1  # Índice 1
    ii = 2  # Índice 2

    while i <= size and ii <= size:

        video = lt.getElement(ord_videos, i)
        video['dias_t'] = 1

        if video[llave] == lt.getElement(ord_videos, ii)[llave]:  # Si video tiene el mismo título que el siguiente vídeo.

            while ii <= size and (video[llave] == lt.getElement(ord_videos, ii)[llave]):  # Mientras el siguiente vídeo tenga el mismo título.
                video['dias_t'] += 1
                ii += 1  # El índice 2 va aumentando.

        # Cuando termine el ciclo
        i = ii
        ii += 1

        # Compara los días trending con más días
        if video['dias_t'] >= mas_dias:
            mas_dias = video['dias_t']
            video_con_mas_dias = video

    return video_con_mas_dias



# Funciones utilizadas para comparar elementos dentro de una lista



def categoryNameToID(catalog, name: str):
    """
    Args:
        catalog: Catálogo ordenado según los Títulos
        name: Nombre de la categoría, para encotrar así su ID.

    Return:
        tupla: Con el nombre de la categoría y su respectivo ID.
    """

    id_ = None

    for llave in lt.iterator(mp.keySet(catalog['category_id'])):  # iteramos por las categorías del catálogo princpal

        category = mp.get(catalog['category_id'], llave)['value']

        if category['name'].lower() == name.lower():

            id_ = int(category['category_id'])
            name = category['name']

            return (id_, name)




def categoryIDtoName(catalog, id_):
    """
    Args:
        catalog: 

    Return:
        tupla: Con el nombre de la categoría y su respectivo ID.
    """
    name = None

    for llave in lt.iterator(mp.keySet(catalog['category_id'])):  # iteramos por las categorías del catálogo princpal

        category = mp.get(catalog['category_id'], llave)['value']

        if category['category_id'] == id_:

            id_ = int(category['category_id'])
            name = category['name']
            return (id_, name)


    if name is None:

        return (id_, name)



def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'views'
        video2: informacion del segundo video que incluye su valor 'views'
    Return:
        bool
    """
    return (float(video1['views']) > float(video2['views']))




def cmpByCountry(name, country):
    """
    Devuelve cero (0) si...
    """
    catentry = me.getKey(country)
    if (name.lower() == catentry.lower()):
        return 0
    elif (name.lower() > catentry.lower()):
        return 1
    else:
        return -1




def cmpCategoriasByName(name, category):
    catentry = me.getKey(category)
    if (name == catentry):
        return 0
    elif (name > catentry):
        return 1
    else:
        return -1




def cmpVideosByTitle(video1, video2):
    return (video1['title'] >= video2['title'])




def cmpDiasTrending(video1, video2):
    return (video1['dias_t'] > video2['dias_t'])




def cmpVideosByLikes(video1, video2):
    return (video1['likes'] > video2['likes'])




def cmpVideosByID(video1, video2):
    return (video1['video_id'] >= video2['video_id'])



# Funciones de ordenamiento



def sortVideos(catalog, cmp: int):
    """
    Args:
        catalog: Catálogo ordenado según los Títulos
        cmp: (1) cmpVideosByViews (2) cmpVideosByTitle (3) cmpVideosByID (4) cmpVideosByLikes

    Return:
        list: Lista ordenada de acuerdo a los parámetros.
    """

    sub_list = lt.subList(catalog['videos'], 1, lt.size(catalog['videos']))
    sub_list = sub_list.copy()

    if cmp == 1:
        sorted_list = mergesort.sort(sub_list, cmpVideosByViews)

    elif cmp == 2:
        sorted_list = mergesort.sort(lst=sub_list, cmpfunction=cmpVideosByTitle)

    elif cmp == 3:
        sorted_list = mergesort.sort(lst=sub_list, cmpfunction=cmpVideosByID)

    else:
        sorted_list = mergesort.sort(lst=sub_list, cmpfunction=cmpVideosByLikes)

    return sorted_list
