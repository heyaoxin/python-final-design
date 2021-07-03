from pypinyin import lazy_pinyin


def Zh2pinying(zh):
    pinyin_arr = lazy_pinyin(zh)
    pinying = ''
    for one in pinyin_arr:
        pinying += one
    return pinying
