import re
def test(str_num):
        if str_num.isdigit():
            return int(str_num)
        out = re.compile("\(.+\)")
        m = out.search(str_num)
        tmp = m.group().strip('()')
        if tmp.isdigit():
            return int(tmp)
        else:
            if ',' in tmp :
                tmp = tmp.strip('k')
                l = tmp.split(',')
                num = int(l[0]) * 1000 + int(l[1]) * 10 ** (3 - len(l[1]))
                return num
            else :
                tmp = tmp.strip('k')
                return int(tmp) * 1000 
print(test("11"))