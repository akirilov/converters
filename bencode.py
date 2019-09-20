# JSON <-> bencode converter

import sys
import json

# Recursively python object into bencode format
def encode(obj):
    to = type(obj)
    if to is str:
        # encode string
        return str(len(obj)) + ':' + obj
    elif to is int:
        # encode int
        return 'i' + str(obj) + 'e'
    elif to is list:
        # encode list
        ret = 'l'
        for li in obj:
            ret += encode(li)
        ret += 'e'
        return ret
    elif to is dict:
        # encode dictionary
        ret = 'd'
        for dk in obj:
            ret += encode(dk) + encode(obj[dk])
        ret += 'e'
        return ret
    else:
        raise TypeError('Incompatible type: ' + str(type(obj)))

# Recursively decode bencode string into python object
def decode(data):
    ret = None
    if data[0] == 'd':
        # decode dictionary
        data = data[1:]
        ret = {}
        while (data[0] != 'e'):
            key,data = decode(data)
            val,data = decode(data)
            ret[key] = val
        data = data[1:]
    elif data[0] == 'l':
        # decode list
        data = data[1:]
        ret = []
        while (data[0] != 'e'):
            val,data = decode(data)
            ret.append(val)
        data = data[1:]
    elif data[0] == 'i':
        # decode int
        end = str.find(data, 'e')
        ret = int(data[1:end])
        data = data[end+1:]
    else:
        # decode string
        col = str.find(data, ':')
        slen = int(data[0:col])
        end = col+slen+1
        ret = data[col+1:end]
        data = data[end:]

    return ret, data

def j2b(s_json):
    obj = json.loads(s_json)
    return encode(obj)

def b2j(s_bcode):
    val,_ =decode(s_bcode)
    return json.dumps(val)

if __name__ == '__main__':
    if sys.argv[1] == 'e':
        print(j2b(sys.stdin.read()))
    elif sys.argv[1] == 'd':
        print(b2j(sys.stdin.read()))
