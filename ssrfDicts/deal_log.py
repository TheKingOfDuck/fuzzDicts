def ddddd(dic):
    o = []
    with open(dic) as f:
        o = f.readlines()
    print len(o)
    o = sorted(list(set(o)))
    print len(o)
    # with open(dic, 'w') as f:
    #     for i in o:
    #         f.write(i)


if __name__ == '__main__':
    ddddd('./ssrf.dic')
    pass
