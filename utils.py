import re
from datetime import datetime

def camel_to_normal(camel):
    split = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', camel)).split()
    ret = " "
    for s in split:
        ret += s[0].upper() + s[1:] + " "
    
    return ret.rstrip()

def normal_to_snake(normal):
    split = normal.split()
    ret = ""
    for s in split:
        ret += s.lower() + '_'
    debug_log(ret[:-1])
    return ret[:-1]

def result_to_dict(result):
    keys = result.keys()
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]

    return keys, items

def debug_log(s):
    with open('debug.txt', 'a') as f:
        f.write(str(datetime.now()) + '\n')
        f.write(s + '\n')

