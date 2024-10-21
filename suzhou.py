from numbers import Real

__all__ = ['suzhou_digit', 'suzhou_numeral_value', 'suzhou', 'to_numeric_type', 'to_int', 'to_decimal_str']

def suzhou_digit(i: int, /, alt: bool = False) -> str:
    if i == 0:
        return '〇'
    elif 1 <= i <= 3 and alt:
        return '一二三'[i - 1]
    elif 1 <= i <= 9:
        return chr(0x3020 + i)
    elif i in {10, 20, 30}:
        return '〸〹〺'[i // 10 - 1]
    else:
        raise ValueError

def suzhou_numeral_value(i: str, /) -> int:
    if i == '〇':
        return 0
    elif i == '一':
        return 1
    elif i == '二':
        return 2
    elif i == '三':
        return 3
    elif '〡' <= i <= '〩':
        return ord(i) - 0x3020
    elif i in '〸十':
        return 10
    elif i in '〹卄':
        return 20
    elif i in '〺卅':
        return 30
    else:
        return ValueError

ZERO = suzhou_digit(0)
ONE = suzhou_digit(1)
TWO = suzhou_digit(2)
THREE = suzhou_digit(3)
FOUR = suzhou_digit(4)
FIVE = suzhou_digit(5)
SIX = suzhou_digit(6)
SEVEN = suzhou_digit(7)
EIGHT = suzhou_digit(8)
NINE = suzhou_digit(9)

ONE_ALT = suzhou_digit(1, True)
TWO_ALT = suzhou_digit(2, True)
THREE_ALT = suzhou_digit(3, True)

TEN = suzhou_digit(10)
TWENTY = suzhou_digit(20)
THIRTY = suzhou_digit(30)

def suzhou(x: Real, /, n: int = None, mag: bool = False, trim_0: bool = True, sign_prefix: str = '－', decimal_point: str = '．') -> str:
    if isinstance(x, str):
        sign_prefix = sign_prefix if x[0] == '-' else ''
        x = x.lstrip('-+')
    else:
        sign_prefix = sign_prefix if x < 0 else ''
        
        if n and not isinstance(x, int):
            x = f'{x:.{n}f}'.lstrip('-+')
        else:
            x = str(x).lstrip('-+')
    
    alt = False
    prev_i = '0'
    alt_list = []
    for i in x:
        if i in '123' and prev_i in '123':
            alt = not alt
        else:
            alt = False
        
        alt_list.append(alt)
        
        prev_i = i
    
    map_ = lambda i, alt: '．' if i == '.' else suzhou_digit(int(i), alt)
    returned = f'{sign_prefix}{"".join(map_(i, alt) for i, alt in zip(x, alt_list))}'
    
    if mag:
        line0 = returned
        line1 = '　' if sign_prefix else ''
        
        mag_n = len(x.split('.')[0])
        
        if 2 <= mag_n <= 4:
            line1 += '十百千'[mag_n - 2]
        elif mag_n >= 5:
            line1 += '　' * (mag_n - 5) + '万'
        
        if trim_0:
            line0 = line0.rstrip("〇")
            if len(line0) < len(line1):
                line0 = f'{line0}{"〇" * (len(line1) - len(line0))}'
        
        if line0.endswith(decimal_point):
            line0 = f'{line0}〇'
        
        return f'{line0}\n{line1}'
    else:
        if returned.endswith(decimal_point):
            returned = f'{returned}〇'
        
        return returned

def to_numeric_type(x: str, /, type_: type = int):
    x = x.splitlines()
    line0 = x[0]
    
    if line0[0] in '-－':
        line0 = line0[1:]
        negative = True
        strip = True
    else:
        negative = False
        if line0[0] in '+＋':
            line0 = line0[1:]
            strip = True
        else:
            strip = False
    
    shift = 0
    if len(x) >= 2:
        line1 = x[1]
        
        if strip:
            line1 = line1[1:]
        
        for i, char in enumerate(line1):
            if line0[i] in '.．':
                break
            
            if char == '　':
                shift += 1
            else:
                if char in '〸十拾':
                    shift += 1
                elif char in '百佰':
                    shift += 2
                elif char in '千仟':
                    shift += 3
                elif char in '万萬':
                    shift += 4
                elif char in '毛毫':
                    shift -= 1
                break
    
    if shift:
        returned = ''
        for i in line0:
            if i in '.．':
                continue
            
            returned = f'{returned}{suzhou_numeral_value(i)}'
            if shift == 0:
                returned += '.'
            
            shift -= 1
        
        return type_(f'{"-" if negative else ""}{returned}{"0" * (shift + 1)}')
    else:
        return type_(f'{"-" if negative else ""}{"".join("." if i in ".．" else str(suzhou_numeral_value(i)) for i in line0)}')

def to_int(x: str, /) -> int:
    return to_numeric_type(x)

def to_decimal_str(x: str, /) -> str:
    return to_numeric_type(x, str)
