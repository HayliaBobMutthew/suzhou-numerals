import unicodedata
import math

def get_suzhou_digit(i: int, /, alt: bool=False) -> str:
    if i == 0:
        return '\u3007'
    elif 1 <= i <= 3 and alt:
        return '\u4e00\u4e8c\u4e09'[i-1]
    elif 1 <= i <= 9:
        return chr(0x3020 + i)
    elif i == 10:
        return '\u3038'
    elif i == 20:
        return '\u3039'
    elif i == 30:
        return '\u303a'
    else:
        raise ValueError

def to_suzhou(x: int, /, mag: bool=False, unit: str=None) -> str:
    n = int(math.log10(abs(x))) + 1 if abs(x) else 1
    
    alt = False
    last_i = 0
    returned = '\uff0d' if x<0 else ''
    
    for k in reversed(range(n)):
        i = x // 10**k % 10
        
        if 1 <= i <= 3 and 1 <= last_i <= 3:
            alt = not alt
        else:
            alt = False
        
        returned += get_suzhou_digit(i, alt)
        
        last_i = i
    
    if mag is not None or unit is not None:
        bottom_line = '\u3000' if x<0 else ''
        
        if mag:
            if n <= 1:
                pass
            elif n == 2:
                bottom_line += '\u5341'
            elif n == 3:
                bottom_line += '\u767e'
            elif n == 4:
                bottom_line += '\u5343'
            elif n == 5:
                bottom_line += '\u4e07'
        
        if unit is not None:
            bottom_line += unit
            
        returned += '\n' + bottom_line
    
    return returned

def to_int(x: str, /) -> int:
    x = x.splitlines()
    
    returned = sum(int(unicodedata.numeric(i)) * 10**k for k, i in enumerate(reversed(x[0])))
    
    if len(x) >= 1:
        mag = x[1][0]
        mag_value = 1
        
        if mag in {TEN, '\u5341'}:
            mag_value = 10
        elif mag == '\u767e':
            mag_value = 100
        elif mag == '\u5343':
            mag_value = 1000
        elif mag in {'\u4e07', '\u842c'}:
            mag_value = 10000
            
        returned *= mag_value
    else:
        return returned

def to_float(x: str, /) -> float:
    x = x.splitlines()
    
    returned = sum(unicodedata.numeric(i) * 10**k for k, i in enumerate(reversed(x[0])))
    
    if len(x) >= 1:
        mag = x[1][0]
        mag_value = 1.0
        
        if mag in TEN + '\u5341':
            mag_value = 10.0
        elif mag == '\u767e':
            mag_value = 100.0
        elif mag == '\u5343':
            mag_value = 1000.0
        elif mag in '\u4e07\u842c':
            mag_value = 10000.0
        elif mag in '\u6bdb\u6beb':
            mag_value = 0.1
            
        returned *= mag_value
    else:
        return returned

ZERO = get_suzhou_digit(0)
ONE = get_suzhou_digit(1)
TWO = get_suzhou_digit(2)
THREE = get_suzhou_digit(3)
FOUR = get_suzhou_digit(4)
FIVE = get_suzhou_digit(5)
SIX = get_suzhou_digit(6)
SEVEN = get_suzhou_digit(7)
EIGHT = get_suzhou_digit(8)
NINE = get_suzhou_digit(9)

ONE_ALT = get_suzhou_digit(1, True)
TWO_ALT = get_suzhou_digit(2, True)
THREE_ALT = get_suzhou_digit(3, True)

TEN = get_suzhou_digit(10)
TWENTY = get_suzhou_digit(20)
THIRTY = get_suzhou_digit(30)