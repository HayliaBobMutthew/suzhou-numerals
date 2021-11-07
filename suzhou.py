import unicodedata

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

def to_suzhou(x: int, /) -> str:
    n = len(str(x))
    
    alt = False
    last_i = 0
    returned = ''
    
    for k in reversed(range(n)):
        i = x // 10**k % 10
        
        if 1 <= i <= 3 and 1 <= last_i <= 3:
            alt = not alt
        else:
            alt = False
        
        returned += get_suzhou_digit(i, alt)
        
        last_i = i
    
    return returned

def to_int(x: str, /) -> int:
    return sum(int(unicodedata.numeric(i)) * 10**k for k, i in enumerate(reversed(x)))

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