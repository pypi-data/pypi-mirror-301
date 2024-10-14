# Copyright (C) 2024 <UTN FRA>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tabulate import tabulate as tabu
from ..utn_funciones.auxiliares import saludo
from .matriz_pp import matriz_concesionaria

saludo(False)

def get_original_matrix() -> list[list]:
    """
    :summary:
    
    La función `get_original_matrix()` devuelve la matriz original de una variable llamada
    `matriz_concesionaria`.
    
    :return: La función `get_original_matrix()` devuelve una lista de listas que representan la matriz original
    de una concesionaria de autos usados llamada `matriz_concesionaria`.
    
    ejemplo:
    
        matriz_concesionaria = [
        autos_marcas,       # Las marcas de los autos
        autos_modelos,      # Los modelos de los autos
        autos_cantidades,   # Las cantidades disponibles en el garage
        autos_precios,      # Los precios unitarios
        autos_ganancias     # El total netro entre cantidades y precio unit. (sin calcular)
    ]
    """
    return matriz_concesionaria

def mostrar_matriz_texto_tabla(matrix: list[list], nombres_columnas: list[str], tablefmt: str = 'rounded_grid') -> None:
    """
    La función `mostrar_matriz_texto_tabla` muestra una matriz como una tabla de texto formateada con encabezados
    en Python.

    :param matrix: El parámetro `matrix` es una lista de listas que representan los datos que desea
    mostrar en forma de tabla. Cada lista interna representa una fila en la tabla y los elementos dentro de cada
    lista interna representan las columnas de la tabla.
    :type matrix: list[list]
    
    `IMPORTANTE`
    la matríz de la concesionaria **deberia** tener un formato estilo:
    
    matriz = [
        \n['Indice Garage', 'Marca', 'Modelo', 'Unidades', 'Precio', 'Ganancia'],
        \n['Indice Garage', 'Marca', 'Modelo', 'Unidades', 'Precio', 'Ganancia']
    \n]
    
    :param nombres_columnas: El parámetro `nombres_columnas` es una lista de cadenas que representan los encabezados de columna de la tabla.
    Cada cadena en la lista corresponde a una columna en la tabla y proporciona una etiqueta para esa columna.
    :type nombres_columnas: list[str]
    :param tablefmt: El parámetro `tablefmt` especifica el formato de la tabla que se mostrará. Determina el estilo y la apariencia de la tabla cuando se imprime. Algunos valores comunes para
    `tablefmt` incluyen 'plain', 'simple', 'grid', 'pipe', 'orgtbl', 'jira', ', el valor predeterminado es rounded_grid
    :type tablefmt: str (opcional)
    
    :ejemplo:
    
    
    """
    text = tabu(matrix, nombres_columnas, tablefmt, numalign = 'right')
    print(text)

