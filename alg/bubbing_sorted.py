'''
    冒泡排序
'''

ary = [5,2,1,6,3,9]

def sort_ary(ary):

    n = len(ary)

    while n > 1:
        i = 1
        while i < n:
            if ary[i] < ary[i-1]:
                ary[i], ary[i-1] = ary[i-1], ary[i]
            i += 1
        n -= 1


    print(ary)


sort_ary(ary)
