
def guess_charset(data):
    f = lambda d, enc: d.decode(enc) and enc

    try: return f(data, 'utf-8')
    except: pass
    try: return f(data, 'cp932')
    except: pass
    try: return f(data, 'shift-jis')
    except: pass
    try: return f(data, 'euc-jp')
    except: pass
    try: return f(data, 'iso2022-jp')
    except: pass
    return None


def safe_decode(data, default=None):
    charset = guess_charset(data) or default
    if charset:
        return data.decode(charset,'replace')
    return data


