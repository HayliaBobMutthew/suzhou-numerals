from decimal import Decimal, localcontext

def suzhou_digit(i: int, /, alt: bool=False) -> str:
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

def suzhou_digit_to_int(i: str, /) -> int:
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
    elif i in '〸〹〺':
        return 10 * (ord(i) - 0x3038 + 1)
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

def suzhou(x: int, /, mag: bool=False, unit: str=None, sign_prefix: str='－') -> str:
    sign = -1 if x < 0 else 1
    
    x = str(abs(x))
    n = len(x)
    
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
    
    returned = (sign_prefix if sign == -1 else '') + ''.join(suzhou_digit(int(i), alt) for i, alt in zip(x, alt_list))
    
    if mag or unit:
        line0 = returned
        line1 = '　' if sign == -1 else ''
        
        if mag:
            if 2 <= n <= 4:
                line1 += '十百千'[n - 2]
            elif n >= 5:
                line1 += '　' * (n - 5) + '万'
        
        if unit:
            line1 += unit
        
        trim_zeros = line0.rstrip('〇')
        if line0 != trim_zeros:
            line0 = trim_zeros + '〇'
            
            if len(line0) != len(line1):
                line0 += '〇' * (len(line1) - len(line0))
        
        returned = line0 + '\n' + line1
    
    return returned

def to_numeric(x: str, /, type_=int):
    x = x.splitlines()
    line0 = x[0]
    
    if line0[0] in '-－負':
        line0 = line0[1:]
        sign = -1
    else:
        sign = 1
    
    mag_value = 1
    if len(x) >= 2:
        line1 = x[1]
        
        if sign == -1:
            line1 = line1[1:]
        
        mag = line1[0]
        
        if mag in '〸十拾':
            mag_value = 10
        elif mag in '百佰':
            mag_value = 100
        elif mag in '千仟':
            mag_value = 1000
        elif mag in '万萬':
            mag_value = 10000
        elif mag in '毛毫':
            if type_ != int:
                mag_value = type_('0.1')
            else:
                mag_value = 0.1
    
    returned = sum(suzhou_digit_to_int(i) * 10**k for k, i in enumerate(reversed(line0)))
    
    if type_ == Decimal:
        with localcontext(prec=len(line0)) as ctx:
            return +(Decimal(returned) * mag_value * sign)
    else:
        return type_(returned * mag_value * sign)

def to_int(x: str, /) -> int:
    return to_numeric(x)
