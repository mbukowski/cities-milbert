import re

def unit_name(name: str) -> str:
    res = name
    res = re.sub(' - miasto.*', '', res)
    res = re.sub(' od.*', '', res)
    res = re.sub(' do.*', '', res)

    return res
