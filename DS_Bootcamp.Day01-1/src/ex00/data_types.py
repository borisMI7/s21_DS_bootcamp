def data_types():
    i = 1
    s = "hello"
    f = 1.0
    b = True
    l = [1, 2, 3]
    d = {'a':1, 'b':2}
    t = (1, 2, 3)
    st = {1, 2, 3}
    variables = [i, s, f, b, l, d, t, st]
    types = [type(var).__name__ for var in variables]

    print('[' + ', '.join(types) + ']')

if __name__ == '__main__':
    data_types()