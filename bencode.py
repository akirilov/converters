import sys
import json

def encode(obj):
    to = type(obj)
    if to is str:
        return str(len(obj)) + ':' + obj
    elif to is int:
        return 'i' + str(obj) + 'e'
    elif to is list:
        ret = 'l'
        for li in obj:
            ret += encode(li)
        ret += 'e'
        return ret
    elif to is dict:
        ret = 'd'
        for dk in obj:
            ret += encode(dk) + encode(obj[dk])
        ret += 'e'
        return ret
    else:
        raise TypeError('Incompatible type: ' + str(type(obj)))

def decode(data):
    ret = None
    if data[0] == 'd':
        data = data[1:]
        ret = {}
        while (data[0] != 'e'):
            key,data = decode(data)
            val,data = decode(data)
            ret[key] = val
        data = data[1:]
    elif data[0] == 'l':
        data = data[1:]
        ret = []
        while (data[0] != 'e'):
            val,data = decode(data)
            ret.append(val)
        data = data[1:]
    elif data[0] == 'i':
        # int decode
        end = str.find(data, 'e')
        ret = int(data[1:end])
        data = data[end+1:]
    else:
        # string decode
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
    return val

if __name__ == '__main__':
    if sys.argv[1] == 'e':
        print(j2b(sys.stdin.read()))
    elif sys.argv[1] == 'd':
        print(b2j(sys.stdin.read()))
