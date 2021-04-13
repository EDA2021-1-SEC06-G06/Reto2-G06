"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""



def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- REQ. 1: Encontrar buenos videos por categoría y país")
    print("3- REQ. 2: Encontrar video tendencia por país")
    print("4- REQ. 3: Encontrar video tendencia por categoría")
    print("5- REQ. 4: Buscar los videos con más Likes")
    print("0- Salir")




def printResults(ord_videos, sample=10):
    """
    Args:
        ord_videos: Catálogo de videos ordenados.
        sample: cantidad de videos para imprimir.
    """
    size = lt.size(ord_videos)

    if size > sample:
        print("Los primeros {0} vídeos ordenados son:\n".format(sample))

        i = 1

        while i <= sample:

            video = lt.getElement(ord_videos, i)

            print("Fecha de tendencia: {0}   Título: {1}   Canal: {2}   Fecha de publicación: {3}   Visitas: {4}   Likes: {5}   Dislikes: {6}\n".format(video['trending_date'], video['title'], video['channel_title'], video['publish_time'], video['views'], video['likes'], video['dislikes']))

            i += 1




def printReqCuatro(ord_videos, sample=10):
    """
    Args:
        ord_videos: Catálogo de videos ordenados.
        sample: cantidad de videos para imprimir.

    Imrpime el requerimiento 4
    """
    size = lt.size(ord_videos)

    if size > sample:
        print("Los primeros {0} vídeos ordenados son:\n".format(sample))

        i = 1

        while i <= sample:
            video = lt.getElement(ord_videos, i)

            print("Título: {0}   Canal: {1}   Fecha de publicación: {2}   Visitas: {3}   Likes: {4}   Dislikes: {5}   Tags: {6}\n".format(video['title'], video['channel_title'], video['publish_time'], video['views'], video['likes'], video['dislikes'], video['tags']))

            i += 1




def printCountryData(country):
    """
    Args:
        country: Nombre del país.

    Imrpime el país y la cantidad de vídeos en ese país.
    """

    if country:
        print("Nombre del país: {0}\n".format(country['name']))
        print('Cantidad de vídeos en este país: {0}\n'.format(lt.size(country['videos'])))
    else:
        print("No se encontró el país")




def printCategoryData(category):
    """
    Args:
        category: Nombre de la categría.

    Imrpime la categoría y la cantidad de vídeos en esa categoría.
    """
    if category:
        print('Nombre de la categoría: {0}\n'.format(category['name']))
        print("Cantidad de vídeos en la categoría: {0}\n".format(lt.size(category['videos'])))
    else:
        print("No se encontró")




def printPrimerVideo(video):
    """
    Args:
        video: Nombre del primer video cargado en el catálogo.

    Return:
        video1: Retorna el primero video cargado en el catálogo.
    """

    if video:
        return("Fecha de tendencia: {0}   Título: {1}   Canal: {2}   Fecha de publicación: {3}   Visitas: {4}   Likes: {5}   Dislikes: {6}".format(video['trending_date'], video['title'], video['channel_title'], video['publish_time'], video['views'], video['likes'], video['dislikes']))
    else:
        return("No se encontró el primero video")




def printCategoryID(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Imprime el nombre y el ID de la categoría.
    """
    if catalog:
        print("El ID y el nombre de las categorias el lo siguiente:\n")
        categories = catalog["category_id"]
        for llave in lt.iterator(mp.keySet(categories)):

            category = mp.get(categories, llave)['value']  # Ejemplo: {'key': 'Entertainment', 'value': {'name': 'Entertainment', 'category_id': 24}}

            print("{0} --- {1}".format(category['category_id'], category['name']))



def initCatalog(factorcarga: int):
    """
    Inicializa el catálogo de videos.
    """
    return controller.initCatalog(factorcarga)


def loadData(catalog):
    """
    Args:
        catalog: Catálogo de videos.
    Carga los videos en la estructura de datos.
    """
    controller.loadData(catalog)



catalog = None
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)



"""
Menu principal
"""



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')


    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")

        # Se inicializa el catálogo.
        catalog = initCatalog(0.30)

        # Se cargan los videos en la estructura de datos.
        loadData(catalog)

        print(catalog['categories'])

        print("Videos cargados: {0}".format(lt.size(catalog['videos'])))

        print("Categorías cargadas: {0}".format(mp.size(catalog['category_id'])))

        print("El primero video es:\n{0}\n".format(printPrimerVideo(controller.primerVideo(catalog))))

        printCategoryID(catalog)




    elif int(inputs[0]) == 2:  # Requerimiento 1

        countryName = input("Ingrese el nombre del país que desea:\n~ ")

        categoryName = input("Ingrese el nombre de la categoría que desea:\n~ ")


        categoryCatalog = controller.getVideosByCategoryOrCountry(catalog, categoryName, countryName)  # Mirar parámetros


        printCategoryData(categoryCatalog)  # Se imprime la información filtrada por categoría y país


        cantidad_videos = int(input("Ingrese la cantidad de vídeos que desea listar:\n~ "))


        result = controller.sortVideos(categoryCatalog, 1)  # Ordenamiento por views

        printResults(result, sample=cantidad_videos)




    elif int(inputs[0]) == 3:

        # Funciones del reto 1, las cuales no se han editado para el reto 2.

        countryName = input("Ingrese el nombre del país que le interesa:\n~ ")

        countryCatalog = controller.getVideosByCountry(catalog, countryName)  # Nuevo catálogo filtrado del país elegido

        printCountryData(countryCatalog)

        ordenados = controller.sortVideos(countryCatalog, 2)  # Vídeos ordenados según su ID

        video = controller.masDiasTrending(ordenados, 2)

        print("El vídeo con más días de tendencia en el país {0} fue:\nTítulo: {1} -- Canal: {2} -- País: {3} -- Días de Tendencia: {4}\n".format(countryName, video['title'], video['channel_title'], video['country'], video['dias_t']))



    elif int(inputs[0]) == 4:  # Requerimiento 3

        categoryName = input("Ingrese el nombre de la categoría que le interesa:\n~ ")

        categoryCatalog = controller.getVideosByCategoryOrCountry(catalog, categoryName)  # Catálogo filtrado por la categoría

        printCategoryData(categoryCatalog)

        ordenados = controller.sortVideos(categoryCatalog, 2)  # Vídeos ordenados según su título

        video = controller.masDiasTrending(ordenados, 1)

        print("El vídeo con más días de tendencia en la categoría {0} fue:\nTítulo: {1} -- Canal: {2} -- ID de la Categoría: {3} -- Días de Tendencia: {4}\n".format(categoryName, video['title'], video['channel_title'], video['category_id'], video['dias_t']))



    elif int(inputs[0]) == 5:

        print("\nRequerimiento no completado hasta el momento, seleccione otro.\n")

        # Funciones del reto 1, las cuales no se han editado para el reto 2.

        countryName = input("Ingrese el nombre del país que le interesa:\n~ ")
        tag = input("Ingrese el tag que desea consultar:\n~ ")
        size = int(input("Ingrese la cantidad de vídeos que desea listar:\n~ "))


        tagsCatalog = controller.getVideosByTagCountry(catalog, tag, countryName)

        likesCatalog = controller.sortVideos(tagsCatalog, 4)

        printReqCuatro(likesCatalog, size)



    else:
        sys.exit(0)
sys.exit(0)
