<table>
    <tr>
        <td align='center'>
            <img alt="Logo UTN Large" src="https://github.com/caidevOficial/Logos/blob/master/Personales/Logo_Developer.png?raw=true" href="https://www.utnfravirtual.org.ar/" width="750px"/>
        </td>
    </tr>
</table></br>

### Set de datos con informaci&oacute;n de h&eacute;roes y villanos para los desaf&iacute;os:

- Desafio 02: Matr&iacute;z


## ➡️ Para el Desaf&iacute;o 02:

Te proveemos un gran set de datos de h&eacute;roes, dividido en una matr&iacute;z
para que puedas realizar tus ejercicios.

Para poder usarlos importa en tus modulos lo siguiente

```py
from UTN_Heroes_Dataset.utn_matrices import matriz_data_heroes
```

Dicha matriz esta formada por listas que segun sus indices son las siguientes:

```py
matriz_data_heroes = [
    lista_nombres_heroes,       # NOMBRES (DE HEROE)
    lista_identidades_heroes,   # IDENTIDADES (NOMBRE REAL DEL PERSONAJE)
    lista_apodos_heroes,        # APODO
    lista_generos_heroes,       # GÉNERO
    lista_poder_heroes,         # PODER (ENTERO)
    lista_alturas_heroes        # ALTURA (FLOTANTE)
]
```
A partir de este punto, estas en condiciones de utilizar las listas, imprimirlas, recorrerlas o hacer lo que se te plazca


## 🚀 Extras:

El paquete tiene funciones que pueden utilizar para sus desaf&iacute;os.

```py
from UTN_Heroes_Dataset.utn_funciones import (
    saludo, clear_console, play_sound
)

from UTN_Heroes_Dataset.utn_funciones.auxiliares import color_text
```

Estas funciones pueden usarse como auxiliares.

```py
# color_text retorna un string

color_text('Tu texto', 'Info')
# Salida -> > Information: Tu texto [Pintado de azul/violeta]

color_text('Tu texto', 'Success')
# Salida -> > Success: Tu texto [Pintado de verde]

color_text('Tu texto', 'Error')
# Salida -> > Error: Tu texto [Pintado de rojo]

color_text('Tu texto')
# Salida -> > System: Tu texto [Pintado de rojo]
```

```py
# Esta funcion mostrara por consola el mensaje: "Presiona Enter para continuar...", al presionarla limpiara tu consola sin importar si tu SO es Windows o UNIX
clear_console()
```

```py
# Esta funcion reproduce un sonido que podes usar para darle un lindo efecto a tu aplicacion de consola.
play_sound()
```
---
</br></br></br></br></br>

<table>
    <tr>
        <td align='center'>
            <img alt="Logo UTN Large" src="https://github.com/caidevOficial/Logos/blob/master/Instituciones/desafio2.gif?raw=true" href="https://www.utnfravirtual.org.ar/" width="750px"/>
        </td>
    </tr>
</table></br>

# Enunciado Desaf&iacute;o UTN Industries 2:

### Desde **_UTN Industries_** queremos sacar ciertas métricas de los heroes y villanos. Para ello te guiaremos con algunas descripciones paso a paso de funciones para que puedas desarrollar el programa que nos permita saber lo que necesitamos, si logras hacerlo bien no seras contratado/a, pero quiza Batman te deje sacarte una foto con su Batimovil!
---
## ⚠️ Disclaimer:
### Este desaf&iacute;o es mas complejo ya que te guiaremos muy parcialmente en lo b&aacute;sico que necesitas para armar tu aplicaci&oacute;n. En este caso el men&uacute; y como validar la opci&oacute;n ingresada por el usuario, el resto queda a tu criterio usando muy buenas pr&aacute;cticas, documentando muy bien el c&oacute;digo, creando los paquetes y modulos que creas necesario y realizando bien las importaciones. Si aplicas funciones recursivas, estar&aacute;s m&aacute;s cerca de que Deadpool te invite unas chimichangas.

<br><br><br>

## A - Desarrolla el paquete "validaciones" y modulo "validaciones" para luego...

#### A1 - En el modulo validaciones: Desarrolla la funcion "validar_opcion" la cual tendrá dos parámetros de entrada (un numero minimo y un numero maximo, ambos enteros) y dentro debe pedirle al usuario que ingrese un numero (el cual sera usado para seleccionar alguna opcion del menu principal de la aplicacion). En caso de ingresar un valor incorrecto (algun numero fuera del rango o algo que no sea integramente numeros enteros) la funcion se ejecutara de nuevo a si misma, en caso de elegir una opcion correcta, la retornara COMO UN ENTERO.

## B - Desarrolla el paquete "funciones" con el modulo: "salida_consola" para luego...

#### B1 - En el modulo "salida_consola": Desarrolla la funcion "mostrar_menu" la cual tendra que mostrar el menu de opciones del programa. Dichas opciones son:

##### Nota: Mostrar a X heroe, implica mostrar todos sus datos, formateados en columnas como si de una planilla se tratara.

### Menú
* 1 - Mostrar la cantidad de Heroes Femeninos.
* 2 - Mostrar la cantidad de Heroes Masculinos.
* 3 - Mostrar a los heroes con mas de 75 de poder.
* 4 - Mostrar al/los heroe/s con mas de 160 de altura.
* 5 - Filtrar a los heroes Femeninos con mas de 60 de poder.
* 6 - Filtrar a los heroes Masculinos con menos de 60 de poder.
* 7 - Filtrar a los personajes No-Binarios con poder entre 10 y 50 inclusive.
* 8 - Determinar cual es el minimo de poder y mostrar cuantos heroes tienen un poder igual al minimo.
* 9 - Determinar cual es el maximo de altura y mostrar cuantos heroes tienen dicha altura.
* 10 - Ordenar los heroes Alfabeticamente ASCENDENTE segun su nombre.
* 11 - Ordenar los heroes Alfabeticamente DESCENDENTE segun su apodo.
* 12 - Ordenar los heroes por Altura y que el usuario decida ASC o DES.
* 13 - Salir.