import re

def snake_casify(str):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    
    return pattern.sub('_', str).lower()

# input: integer size in bytes (B)
# return: string formatted size with appropriate B, KB or MB
def str_filesize(b_int):
    b_int = int(b_int)
    if b_int < 1024:
        return '{0:.2f}B'.format(b_int)
    kb_float = b_int / 1024.0
    if kb_float < 1024.0:
        return '{0:.2f}KB'.format(kb_float)
    mb_float = kb_float / 1024.0
    return '{0:.2f}MB'.format(mb_float)
