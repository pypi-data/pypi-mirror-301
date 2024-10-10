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

def mostrar_matriz_texto_tabla(matrix: list[list], nombres_columnas: list[str], tablefmt: str = 'rounded_grid') -> None: ...
def color_text(text: str, message_type: str = '') -> str: ...
def saludo(include_beam: bool = True) -> None: ...
def clear_console() -> None: ...
def get_original_matrix() -> list[list]: ...