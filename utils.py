import re
import json
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
    # debug_log(ret[:-1])
    return ret[:-1]

def normal_to_camel(normal):
    split = normal.split()
    ret = ""
    for s in split:
        if ret == "":
            ret += s.lower()
            continue
        ret += s[0].upper() + s[1:]

    # debug_log(ret)
    return ret

def hyphen_to_camel(hyphen):
    split = hyphen.split('-')
    ret = ""
    for s in split:
        if ret == "":
            ret += s.lower()
            continue
        ret += s[0].upper() + s[1:]

    # debug_log(ret)
    return ret

def result_to_dict(result, PK=None):
    keys = result.keys()
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]

    if PK:
        for i, item in enumerate(items):
            key = {}
            for k in PK:
                key[k] = item[k]
            items[i]['PK'] = str(key)
            # debug_log(str(items[i]))

    return items[0].keys(), items

def fix_nesting(s):
    s = str(s).replace("'", '"')
    s = s.replace('"{', '{')
    s = s.replace('}"', '}')
    return s

def generate_where_from_pk(pks):
    pks = str(pks).replace("'", '"')
    pks = json.loads(pks)
    id = ""
    for k, v in pks.items():
        if any(c.isalpha() for c in str(v)):
            id += f'{k}="{v}" AND '
        else:
            id += f'{k}={v} AND '
    id = id[:-5]
    
    return id

def generate_fields(data):
    fields = ""
    for k, v in data.items():
        if k == 'pk' or k == 'table':
            continue
        if any(c.isalpha() for c in str(v)):
            fields += f'{k}="{v}", '
        else:
            fields += f'{k}={v}, '
    fields = fields[:-2]

    return fields

def debug_log(s):
    with open('debug.txt', 'a') as f:
        f.write(str(datetime.now()) + '\n')
        f.write(s + '\n')

