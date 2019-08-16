'''
快速排序
'''
import random
def quicksort(list):
    if len(list) < 2:
        return list

    midpviot = list[0]
    lessbeforemdpivot = [i for i in list[1:] if i <= midpviot]
    biggeraftermidpivot = [i for i in list[1:] if i > midpviot]
    finallylist = quicksort(lessbeforemdpivot) + [midpviot] + quicksort(biggeraftermidpivot)

    return finallylist


# ls = range(99999)
# ary = list(ls)
# random.shuffle(ary)

ary = [2,1,9,5,3,6,4]

print(ary)

print(quicksort(ary))

