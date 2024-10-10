```
░██████╗░██╗██╗░░░██╗███████╗░█████╗░░█████╗░██╗░░░░░░█████╗░██████╗░
██╔════╝░██║██║░░░██║██╔════╝██╔══██╗██╔══██╗██║░░░░░██╔══██╗██╔══██╗
██║░░██╗░██║╚██╗░██╔╝█████╗░░██║░░╚═╝██║░░██║██║░░░░░██║░░██║██████╔╝
██║░░╚██╗██║░╚████╔╝░██╔══╝░░██║░░██╗██║░░██║██║░░░░░██║░░██║██╔══██╗
╚██████╔╝██║░░╚██╔╝░░███████╗╚█████╔╝╚█████╔╝███████╗╚█████╔╝██║░░██║
░╚═════╝░╚═╝░░░╚═╝░░░╚══════╝░╚════╝░░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝
```

@author: 𓂀 𝒥-𝒳𝒶𝓃𝒹𝑒𝓇 𓂀<br>
@version: 0.1.5<br>
@since: 2024/09/27
@date: 2024/10/7

Imprime texto de colores y con estilos en la terminal

# Funcionalidad
Sobreescribe la funcion interna print y añade nuevos parametro:
- __`fore`__: Recibe un identificador ansi para establecer el color del texto
- __`back`__: Recibe un identificador ansi para establecer un color de fondo el texto.
- __`style`__: Recibe un identificador ansi para establece un stylo en el texto.
> Nota: Puede recibir tanto como un numero como una cadena o la secuencia de escape directa.

__EJEMPLO DE USO__
```py
    import givecolor

    print('Texto en rojo y fondo blanco', fore='red', back='white')
    print('Texto en rojo y fondo blanco', fore=31, back=47)
```
__Podemos importar algunas clases *Enum* perteneciente a la libreria para poder optener una lista de todos los colores y stylos disponibles__
- `Fore`: Enumera los colores de texto disponibles.
- `Back`: Enumera los colores de fondo disponibles.
- `Style`: Enumero los stylos disponibles que podemos darle al texto.
> Nota: Hay varios estilos que no estan añadidos ya que no soportados por ciertas terminales.

__EJEMPLO DE USO__  
```py
    from givecolor import Fore, Back, Style

    print('Texto en verde y tachado con fondo azul',
            fore=Fore.GREEN,
            back=Back.BLUE,
            style=Style.CROSSED)
```

