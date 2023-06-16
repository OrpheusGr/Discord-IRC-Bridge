x = 0
y = "s"
z = True
print(type(type(x)), type(y), type(z))


def totype(of, to):
    if type(of) == int:
        try:
           r = int(to)
        except:
           r = "non_same_type"
    elif type(of) == str:
        try:
           r = str(to)
        except:
           r = "non_same_type"
    elif type(of) == bool:
        if to == "False":
           r = False
        elif to == "True":
           r = "True"
        else:
           r = ""
    return r

x = totype("a", False)
print(x, type(x))
