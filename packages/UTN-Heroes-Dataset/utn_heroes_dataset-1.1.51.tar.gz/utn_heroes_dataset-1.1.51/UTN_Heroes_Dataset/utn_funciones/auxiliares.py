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

import pygame.mixer as mixer
import time
import sys
from .system_pkg import hide_pg_support_message, get_pkg_version
from ..utn_assets import sound_path, desafio_1, desafio_2

from terminaltexteffects.effects import (
    effect_beams, effect_rain, effect_slide
)
import random as rd
from tabulate import tabulate as tabu

def crear_enunciado_desafio_1() -> None:
    """
    The function `crear_enunciado_desafio_1` reads the content from a file named `desafio_1` and writes
    it to a new file named `Desafio_01.md`.
    """
    content = ''
    with open(desafio_1, 'r', encoding='utf-8') as file:
        content = file.read()
    with open('./Desafio_01.md', 'w', encoding='utf-8') as file:
        file.write(content)

def crear_enunciado_desafio_2() -> None:
    """
    This Python function reads the content of a file named `desafio_2` and writes it to a new file named
    `Desafio_02.md`.
    """
    content = ''
    with open(desafio_2, 'r', encoding='utf-8') as file:
        content = file.read()
    with open('./Desafio_02.md', 'w', encoding='utf-8') as file:
        file.write(content)

def color_text(text: str, message_type: str = '') -> str:
    """
    The function `color_text` takes a text input and a message type, and returns the text formatted
    with color based on the message type.
    
    :param text: The `text` parameter in the `color_text` function is the string that you want to
    colorize based on the `message_type`. It is the main content that will be displayed with the
    specified color and message type
    :type text: str
    :param message_type: The `message_type` parameter in the `color_text` function is used to specify
    the type of message being displayed. It has a default value of an empty string, which means if no
    message type is provided when calling the function, it will default to a general system message
    :type message_type: str
    """
    _b_red: str = '\033[41m'
    _b_green: str = '\033[42m'
    _b_blue: str = '\033[44m'
    _f_white: str = '\033[37m'
    _no_color: str = '\033[0m'
    message_type = message_type.strip().capitalize()
    match message_type:
        case 'Error':
            text =  f'{_b_red}{_f_white}> Error: {text}{_no_color}'
        case 'Success':
            text = f'{_b_green}{_f_white}> Success: {text}{_no_color}'
        case 'Info':
            text = f'{_b_blue}{_f_white}> Information: {text}{_no_color}'
        case _:
            text =  f'{_b_red}{_f_white}> System: {text}{_no_color}'

    return text

def mostrar_texto_con_efecto(texto: str, include_beam: bool = False) -> None:
    """
    This Python function selects a random text effect and displays the given text with that effect in
    the terminal.
    
    :param texto: The code you provided seems to be a function that takes a text input and applies a
    random visual effect to it before displaying it. The `mostrar_texto_con_efecto` function randomly
    selects an effect from a list ('Slide', 'Beam', 'Rain')
    :type texto: str
    """
    effects = ['Beam', 'Rain', 'Slide']
    if not include_beam: effects.pop(0)
    effect_selected = rd.choice(effects)
    match effect_selected:
        case 'Beam':
            effect = effect_beams.Beams(texto,)
        case 'Rain':
            effect = effect_rain.Rain(texto)
        case 'Slide':
            effect = effect_slide.Slide(texto)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)
            time.sleep(0.01)

def clear_console() -> None:
    """
    The function `clear_console` clears the console screen and prompts the user to press Enter to
    continue.
    """
    import os
    _ = input(color_text("\nPresiona Enter para continuar..."))
    os.system('cls' if os.name in ['nt', 'dos'] else 'clear')

def play_sound() -> None:
    """
    The `play_sound` function initializes the mixer, loads a sound file, sets the volume to 0.4, and
    plays the sound.
    """
    if not mixer.get_init():
        mixer.init()
    mixer.music.load(sound_path)
    mixer.music.set_volume(0.4)
    time.sleep(0.4)
    mixer.music.play()

def saludo(include_beam: bool = True) -> None:
    """
    The function `saludo()` prints a greeting message with information about the UTN community and
    dataset version.
    """
    hide_pg_support_message()
    play_sound()
    message =\
        f"UTN-Heroes-Dataset (v{get_pkg_version()}, Python {'.'.join([str(num) for num in sys.version_info[0:3]])})"\
        f'\nHello from the UTN community. https://pypi.org/project/UTN-Heroes-Dataset/'
    mostrar_texto_con_efecto(message, include_beam)

def mostrar_texto_table(matrix: list[list], headers: list[str], tablefmt: str = 'rounded_grid') -> None:
    """
    The function `mostrar_texto_table` displays a matrix as a formatted table with headers in Python.
    
    :param matrix: The `matrix` parameter is a list of lists that represents the data to be displayed in
    the table. Each inner list corresponds to a row in the table, and the elements within each inner
    list represent the columns of the table
    :type matrix: list[list]
    :param headers: The `headers` parameter is a list of strings that represent the column headers of
    the table. Each string in the list corresponds to a column in the table and provides a label for
    that column
    :type headers: list[str]
    :param tablefmt: The `tablefmt` parameter in the `mostrar_texto_table` function is used to specify
    the format of the table that will be displayed when the function is called. It determines the style
    and appearance of the table output. In this case, the default value for `tablefmt` is set, defaults
    to rounded_grid
    :type tablefmt: str (optional)
    """
    text = tabu(matrix, headers, tablefmt, numalign = 'right')
    print(text)

def create_matrix_by_hero(matrix: list[list]) -> list[list]:
    """
    The function `create_matrix_by_hero` takes a matrix as input and returns a new matrix where the rows
    are transformed into columns.
    
    :param matrix: The `create_matrix_by_hero` function takes a matrix as input, which is a list of
    lists. Each inner list represents a row in the matrix. The function then creates a new matrix where
    the rows become columns and vice versa
    :type matrix: list[list]
    :return: The function `create_matrix_by_hero` is returning a transposed matrix, where the rows of
    the input matrix become the columns of the output matrix and vice versa.
    """
    
    amount_columns = len(matrix[0])
    
    final_matrix = [
        [index_column + 1] + [
            matrix[index_row][index_column] for index_row in range(len(matrix))
        ] for index_column in range(amount_columns)
    ]
    
    return final_matrix
