import os
import chardet
import pandas as pd
import numpy as np

def crear_carpeta(ruta_base, nombre_carpeta):
    """
    Crea una carpeta dada la ruta base y el nombre deseado

    Args:
        ruta_base(str): Ruta de la carpeta raíz
        nombre_carpeta(str): Nombre deseado para la carpeta
    Returns:
        str: Ruta completa de la carpeta creada
    """
    try:
        ruta_completa = os.path.join(ruta_base, nombre_carpeta)
        os.makedirs(ruta_completa, exist_ok=True)
        print(f"Carpeta creada en: {ruta_completa}")
        return ruta_completa
    except Exception as e:
        print(f"Ocurrió un error al crear la carpeta: {e}")

def save_array(path, file_name, array):
    """
    Guarda un array en formato .npy en la ruta especificada.

    Parámetros:
    path (str): La ruta completa, incluyendo el nombre del archivo donde se guardará el array.
    file_name (str): Nombre con el que se desea guardar el archivo
    array (numpy.ndarray): El array que se desea guardar.

    Ejemplo:
    save_array('ruta/al/archivo.npy', mi_array)
    """
    try:
        file_path = os.path.join(path, f'{file_name}.npy')
        np.save(file_path, array)
        print(f"Array guardado exitosamente en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el array: {e}")

def read_codificated_csv(path):
    """
    Detecta la codificación del archivo .csv y lo lee utilizando esa codificación
    Args:
        path(str): Ruta al archivo .csv
    Returns:
        df(pd.DataFrame): Dataframe leído
    """
    with open(fr'{path}', 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(fr'{path}', encoding=result['encoding'])