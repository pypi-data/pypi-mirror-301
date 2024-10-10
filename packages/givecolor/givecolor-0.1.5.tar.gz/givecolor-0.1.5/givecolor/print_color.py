import builtins
import re
from .color import Style, Fore, Back, DEFAULT, ESCAPE


class Colored():
    def __init__(self) -> None:
        """Almacena la fucion print original en original_print y la sustitulle con color_print la cual tiene soporte para imprimir texto y fondos de distintos colores y estilos"""
        self.original_print = builtins.print
        builtins.print = self.color_print

    dic_fore = {
        'BLACK': Fore.BLACK,
        'RED': Fore.RED,
        'GREEN': Fore.GREEN,
        'YELLOW': Fore.YELLOW,
        'BLUE': Fore.BLUE,
        'MAGENTA': Fore.MAGENTA,
        'CYAN': Fore.CYAN,
        'WHITE': Fore.WHITE
    }

    dic_back = {
        'BLACK': Back.BLACK,
        'RED': Back.RED,
        'GREEN': Back.GREEN,
        'YELLOW': Back.YELLOW,
        'BLUE': Back.BLUE,
        'MAGENTA': Back.MAGENTA,
        'CYAN': Back.CYAN,
        'WHITE': Back.WHITE
    }

    dic_style = {
        'BOLD': Style.BOLD,
        'DIM': Style.DIM,
        'UNDELINED': Style.UNDELINED,
        'CROSSED': Style.CROSSED
    }
    
    def color_print(self,
                    *values: object,
                    fore: str = DEFAULT,        # COLOR DEL TEXTO
                    back: str = DEFAULT,        # COLOR DEL FONDO
                    style: str = DEFAULT,       # ESTILO DEL TEXTO
                    sep: str = ' ',
                    end: str = '\n',
                    **kwargs) -> None:
        """Función que envolvera al print original de python, contiene atributos especiales que permite cambiar el color, estilo y el fondo de los mensajes que se imprimen en cosola"""

        if fore == DEFAULT and back == DEFAULT and style == DEFAULT:
            self.original_print(*values, sep=sep, end=end, **kwargs)
        else:
            # VERIFICANDO COLOR DEL TEXTO
            if fore != DEFAULT:
                if isinstance(fore, str):
                    fore = self.dic_fore.get(fore.upper(), self.identify_ANSII(fore, Fore))
                elif isinstance(fore, int):
                    fore = self.range_int(fore, Fore)
                elif not isinstance(fore, Fore):
                    fore = DEFAULT

            # VERIFICANDO EL COLOR DEL FONDO
            if back != DEFAULT:
                if isinstance(back, str):
                    back = self.dic_back.get(back.upper(), self.identify_ANSII(back, Back))
                elif isinstance(back, int):
                    back = self.range_int(back, Back)
                elif not isinstance(back, Back):
                    back = DEFAULT

            # VERIFICANDO EL ESTILO DEL TEXTO
            if style != DEFAULT:
                if isinstance(style, str):
                    style = self.dic_style.get(style.upper(), self.identify_ANSII(style, Style))
                elif isinstance(style, int):
                    style = self.range_int(style, Style)
                elif not isinstance(style, Style):
                    style = DEFAULT

            self.original_print(self.ansi_sequence(style, back, fore), sep=sep, end=end)
            self.original_print(*values, sep=sep, end='', **kwargs)
            self.original_print(self.ansi_reset())

    def identify_ANSII(self, txt:str, selec_enum) -> int:
        """Verifica si la cadena de texto enviada concuerda con los paratros ANSI del la clase enum correspondiente enviada en el parametro selec_enum y retorna el numero correspondiente"""
        data =  re.fullmatch(r'\033\[([0-9]+)m', txt)
        if data is None :
            data = re.fullmatch(r'([0-9]+)', txt)
            if data is None:
                return DEFAULT
            
        return self.range_int(int(data.group(1)), selec_enum)

    def range_int(self, txt:int, selec_enum) -> int:
        """Verifica si el numero enviado coresponde a los valor ANSI de su resectiva clase en caso de enviarse uno que no corresponda retorna el valor por defecto"""
        for enum in selec_enum:
            if enum.value == txt:
                return txt
            
        return DEFAULT
            
    def ansi_sequence(self, style, back, fore) -> str:
        """Retorna la secuencia ANSII con todos los estilos a aplicar"""
        str_ansi = f'{ESCAPE}[{style}'
        if back != DEFAULT:
            str_ansi += f';{back}'

        if fore != DEFAULT:
            str_ansi += f';{fore}'

        str_ansi += 'm'
        return str_ansi

    def ansi_reset(self) -> str:
        """Retorna la secuencia ANSII pare resetear todos estilos"""
        return f'{ESCAPE}[{DEFAULT}m'
        
        

