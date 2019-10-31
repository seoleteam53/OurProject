import re
def test(a):
    return int(re.findall('\d+',a)[0])
print(test("Co binh luan (32)"))