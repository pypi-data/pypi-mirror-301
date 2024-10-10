from enum import Enum

DEFAULT = 0
ESCAPE = '\033'

class Style(Enum):
    BOLD = 1
    DIM = 2
    UNDELINED = 4
    CROSSED = 9

    def __str__(self):
        return str(self.value)

class Fore(Enum):
    """Lista de colores para texto con su respectivo indicador ANSI"""
    
    BLACK  = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    def __str__(self):
        return str(self.value)

class Back(Enum):
    """Lista de colores disponibles para el fondo del texto con su indicador ANSI"""

    BLACK  = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47

    def __str__(self):
        return str(self.value)
    

