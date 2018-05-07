chars = list('u8bd3c1fi7egrham2jlno49kvqt5pxwsz6y0')
number_space = len(chars)
difficulty = 233


def encrypt(symvar):
    code = ''
    source = int(symvar) * difficulty
    while True:
        remainder = source % number_space
        code += chars[remainder]
        source = int(source / number_space)
        if remainder == 0 and source <= 1:
            break
    return code


def decrypt(code):
    resolved = 0
    for index, digit in enumerate(list(code)):
        resolved += chars.index(digit) * number_space ** index
    return str(int(resolved * 1 / difficulty))
