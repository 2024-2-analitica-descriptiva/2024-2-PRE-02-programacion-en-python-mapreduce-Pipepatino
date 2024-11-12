"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
from itertools import groupby
import string
import os
import shutil


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]


def load_input(input_directory):
    """
    Lee todos los archivos en el directorio dado y devuelve una lista de tuplas (nombre_archivo, línea)
    por cada línea de cada archivo.

    Args:
        input_directory (str): El directorio que contiene los archivos a leer.

    Returns:
        list of tuple: Una lista de tuplas donde cada tupla contiene el nombre del archivo y una línea de texto.
                       La tupla tiene la forma (nombre_archivo, línea).
                       Por ejemplo: [('text0.txt', 'Analytics is the discovery...'), ('text1.txt', 'Hypothesis testing...')]

    Raises:
        FileNotFoundError: Si el directorio especificado no existe o no se puede acceder.
        IOError: Si hay problemas al abrir o leer los archivos dentro del directorio.

    Example:
        input_directory = 'data'
        result = load_input(input_directory)
        print(result)
        # Salida: [('text0.txt', 'Analytics is the discovery...'), ('text0.txt', 'in data...')]

    """
    
    result = []
    
    # Obtiene todos los archivos del directorio
    files = glob.glob(f"{input_directory}/*")
    
    # Recorre cada archivo en el directorio
    for file_path in files:
        if os.path.isfile(file_path):  # Verifica si es un archivo
            filename = os.path.basename(file_path)  # Obtiene el nombre del archivo
            with open(file_path, 'r', encoding='utf-8') as file:
                # Lee cada línea del archivo
                for line in file:
                    result.append((filename, line.strip()))  # Añade el nombre del archivo y la línea
    
    return result




#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """
    Preprocesa las líneas de texto: convierte el texto a minúsculas, elimina puntuación y divide las líneas en palabras.

    Esta función recibe una lista de tuplas (nombre_archivo, línea) y realiza el preprocesamiento de las líneas
    para normalizar las palabras. El proceso incluye convertir todo el texto a minúsculas, eliminar caracteres
    de puntuación, y dividir el texto en palabras individuales.

    Args:
        sequence (list of tuple): Una lista de tuplas donde cada tupla contiene el nombre del archivo
                                  y una línea de texto. La tupla tiene la forma (nombre_archivo, línea).

    Returns:
        list of tuple: Una lista de tuplas donde cada tupla contiene el nombre del archivo y una lista de
                       palabras preprocesadas de la línea. La tupla tiene la forma (nombre_archivo, [palabras]).
                       Por ejemplo: [('text0.txt', ['analytics', 'is', 'the', 'discovery']), 
                                    ('text1.txt', ['hypothesis', 'testing', 'for', 'example'])].

    Example:
        sequence = [('text0.txt', 'Analytics is the discovery, in data.'),
                    ('text1.txt', 'Hypothesis testing, for example!')]
        result = line_preprocessing(sequence)
        print(result)
        # Salida: [('text0.txt', ['analytics', 'is', 'the', 'discovery', 'in', 'data']),
        #          ('text1.txt', ['hypothesis', 'testing', 'for', 'example'])]
    
    """
    
    preprocessed = []
    
    for filename, line in sequence:
        # Convertir la línea a minúsculas
        line = line.lower()
        
        # Eliminar puntuación y caracteres no deseados
        line = line.translate(str.maketrans('', '', string.punctuation))
        
        # Dividir la línea en palabras
        words = line.split()
        
        # Agregar la tupla (nombre del archivo, lista de palabras) a la lista de resultados
        preprocessed.append((filename, words))
    
    return preprocessed



#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
    """
    Realiza un conteo de las palabras en la secuencia proporcionada y retorna una lista de tuplas (clave, valor),
    donde la clave es cada palabra y el valor es 1, indicando que la palabra ha sido encontrada una vez.

    La función recibe una lista de tuplas, donde cada tupla contiene un nombre de archivo y una lista de palabras.
    La función recorre todas las palabras de cada archivo y devuelve una lista con tuplas, donde cada tupla tiene la
    palabra como clave y 1 como valor.

    Args:
        sequence (list of tuple): Una lista de tuplas donde cada tupla contiene el nombre del archivo y una lista
                                  de palabras procesadas de ese archivo. La tupla tiene la forma (nombre_archivo, [palabras]).

    Returns:
        list of tuple: Una lista de tuplas donde cada tupla contiene una palabra como clave y el valor es 1. 
                       Por ejemplo: [('analytics', 1), ('is', 1), ('the', 1), ('discovery', 1)].

    Example:
        sequence = [('text0.txt', ['analytics', 'is', 'the', 'discovery']),
                    ('text1.txt', ['hypothesis', 'testing', 'for', 'example'])]
        result = mapper(sequence)
        print(result)
        # Salida: [('analytics', 1), ('is', 1), ('the', 1), ('discovery', 1),
        #          ('hypothesis', 1), ('testing', 1), ('for', 1), ('example', 1)]

    """
    
    result = []
    
    # Recorre cada tupla (nombre del archivo, lista de palabras)
    for filename, words in sequence:
        # Para cada palabra en la lista de palabras
        for word in words:
            result.append((word, 1))  # La clave es la palabra y el valor es 1
    
    return result



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """
    Recibe una lista de tuplas (clave, valor) y devuelve una lista ordenada por la clave (palabra).
    La clave es la palabra y el valor es 1, como en el resultado del mapper.

    Args:
        sequence (list of tuple): Una lista de tuplas donde cada tupla contiene una palabra y el valor 1.
                                  Por ejemplo: [('analytics', 1), ('is', 1), ('the', 1)].

    Returns:
        list of tuple: La lista ordenada por la clave (palabra), manteniendo la estructura de tuplas.
                       Por ejemplo: [('analytics', 1), ('discovery', 1), ('is', 1), ('the', 1)].

    Example:
        sequence = [('is', 1), ('the', 1), ('analytics', 1)]
        result = shuffle_and_sort(sequence)
        print(result)
        # Salida: [('analytics', 1), ('is', 1), ('the', 1)]

    """
    
    # Ordenar la lista por la clave (palabra)
    return sorted(sequence, key=lambda x: x[0])



#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """
    Recibe una lista de tuplas (clave, valor) donde la clave es una palabra y el valor es 1,
    y devuelve una lista de tuplas donde la clave es la palabra y el valor es el total de veces
    que aparece esa palabra en el texto (la suma de los valores asociados a la palabra).

    Args:
        sequence (list of tuple): Una lista de tuplas donde cada tupla contiene una palabra y el valor 1.
                                  La lista está ordenada por la clave. Ejemplo: [('analytics', 1), ('is', 1), ...].

    Returns:
        list of tuple: Una lista de tuplas donde cada tupla contiene una palabra como clave y el total de su
                       aparición como valor. Ejemplo: [('analytics', 3), ('is', 2), ('data', 1)].

    Example:
        sequence = [('analytics', 1), ('is', 1), ('analytics', 1), ('data', 1), ('analytics', 1)]
        result = reducer(sequence)
        print(result)
        # Salida: [('analytics', 3), ('is', 1), ('data', 1)]

    """
    
    reduced_result = []
    
    # Variables para almacenar la palabra actual y su total
    current_word = None
    current_count = 0
    
    # Recorre la lista de tuplas
    for word, count in sequence:
        # Si la palabra cambia, guarda el total de la palabra anterior
        if word == current_word:
            current_count += count  # Sumar 1 para la misma palabra
        else:
            if current_word is not None:
                reduced_result.append((current_word, current_count))  # Guarda la palabra anterior
            current_word = word
            current_count = count  # Reinicia el conteo para la nueva palabra
    
    # Agregar el último grupo de palabras
    if current_word is not None:
        reduced_result.append((current_word, current_count))
    
    return reduced_result



#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#

def create_output_directory(output_directory):
    """
    Crea un directorio de salida. Si el directorio ya existe, lo borra y luego lo crea de nuevo.

    Args:
        output_directory (str): El nombre o ruta del directorio que se debe crear.

    Raises:
        OSError: Si hay problemas al eliminar o crear el directorio.

    Example:
        create_output_directory('output_data')
        # Si 'output_data' existe, será borrado y luego creado nuevamente.
    """
    
    # Verifica si el directorio ya existe
    if os.path.exists(output_directory):
        # Si el directorio existe, lo borra
        shutil.rmtree(output_directory)
    
    # Crea el nuevo directorio
    os.makedirs(output_directory)
    print(f"Directorio '{output_directory}' creado correctamente.")



#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """
    Guarda el resultado del reducer en un archivo de texto llamado 'part-00000'.
    Cada línea del archivo contiene una tupla (clave, valor) donde los elementos están separados por un tabulador.

    Args:
        output_directory (str): El directorio donde se guardará el archivo de salida.
        sequence (list of tuple): La lista de tuplas donde cada tupla contiene una palabra (clave) y su cuenta (valor).
                                  Ejemplo: [('analytics', 3), ('is', 1), ('data', 1)].

    Example:
        save_output('output_data', [('analytics', 3), ('is', 1), ('data', 1)])
        # El archivo 'part-00000' se guardará en el directorio 'output_data'.
    """
    
    # Define the output file path
    output_file_path = os.path.join(output_directory, 'part-00000')
    
    # Open the file in write mode and write the content
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for key, value in sequence:
            # Write each tuple in the format 'key\tvalue' where '\t' is the tab separator
            file.write(f"{key}\t{value}\n")
    
    print(f"Archivo guardado correctamente en '{output_file_path}'.")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """
    Crea un archivo vacío llamado '_SUCCESS' en el directorio especificado para marcar
    que un proceso ha sido completado exitosamente.

    Args:
        output_directory (str): El directorio donde se creará el archivo '_SUCCESS'.

    Example:
        create_marker('output_data')
        # Se crea un archivo vacío '_SUCCESS' en el directorio 'output_data'.
    """
    
    # Define la ruta completa para el archivo '_SUCCESS'
    success_file_path = os.path.join(output_directory, '_SUCCESS')
    
    # Crea el archivo vacío
    with open(success_file_path, 'w', encoding='utf-8'):
        pass  # No hace falta escribir nada, solo crear el archivo vacío
    
    print(f"Archivo '_SUCCESS' creado en '{success_file_path}'.")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """
    Orquesta el flujo de trabajo: carga los archivos, procesa las líneas, cuenta las palabras,
    ordena, reduce el conteo y guarda el resultado en el directorio de salida.

    Args:
        input_directory (str): El directorio que contiene los archivos de entrada.
        output_directory (str): El directorio donde se guardarán los resultados y el archivo '_SUCCESS'.
    
    Example:
        run_job('input_data', 'output_data')
        # El flujo de trabajo se ejecuta y guarda el resultado en 'output_data'.
    """
    
    # Cargar los archivos desde el directorio de entrada
    files = load_input(input_directory)
    
    # Preprocesar las líneas de los archivos cargados
    preprocessed_data = line_preprocessing(files)
    
    # Contar las palabras utilizando el mapper
    mapped_data = mapper(preprocessed_data)
    
    # Ordenar las palabras
    sorted_data = shuffle_and_sort(mapped_data)
    
    # Reducir los datos sumando las ocurrencias de cada palabra
    reduced_data = reducer(sorted_data)
    
    # Guardar el resultado en el archivo de salida
    save_output(output_directory, reduced_data)
    
    # Crear el archivo '_SUCCESS' para marcar el éxito del trabajo
    create_marker(output_directory)
    
    # Mostrar el resultado del trabajo (opcional, puede ser útil para depuración)
    from pprint import pprint
    pprint(reduced_data)
    
    print("El trabajo se completó exitosamente.")


if __name__ == "__main__":
    run_job(
        "files/input",
        "files/output",
    )
