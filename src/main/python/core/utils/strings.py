import re

def snake_casify(str):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    
    return pattern.sub('_', str).lower()