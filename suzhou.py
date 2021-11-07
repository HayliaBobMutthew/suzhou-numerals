def get_suzhou_digit(i: int, /, vertical: bool=True) -> str:
    if i == 0:
        return '\u3007'
    elif 1 <= i <= 3 and not vertical:
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

def suzhou(x, /) -> str:
    n = len(str(x))
    
    vertical = True
    last_i = 0
    returned = ''
    
    for k in range(n-1, 0, -1):
        i = x // 10**k % 10
        
        returned += get_suzhou_digit(i, vertical)
        
        if 1 <= i <= 3 and 1 <= last_i <= 3:
            vertical = not vertical
        else:
            vertical = True
            
        last_i = i
    
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

TEN = get_suzhou_digit(10)
TWENTY = get_suzhou_digit(20)
THIRTY = get_suzhou_digit(30)