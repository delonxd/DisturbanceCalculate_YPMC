from src.AbstractClass.ElePack import *


def show_ele(vessel, para=''):
    if isinstance(vessel, (list, set)):
        list_t = list()
        for ele in vessel:
            if para == '':
                list_t.append(ele.__repr__())
            else:
                list_t.append(ele.__dict__[para].__repr__())
        list_t.sort()
        for ele in list_t:
            print(ele)
    elif isinstance(vessel, (dict, ElePack)):
        keys = sorted(list(vessel.keys()))
        for key in keys:
            if para == '':
                print(key, ':', vessel[key])
            else:
                print(vessel[key].__dict__[para])