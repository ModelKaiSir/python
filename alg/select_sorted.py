import random
'''
    选择排序
    每次取出最小的一个元素放到新元素中
    数据量大的时候性能不好
'''

# ls = range(99999)
# ary = list(ls)

ary = [2,5,1,3,9]

# random.shuffle(ary)

# 找到最小的元素 返回下标
def find_small_ele(a):

    temp = a[0]
    index = -1

    for i, v in enumerate(a):
        if v <= temp:
            temp, index = v, i

    return index

def create_sort_ary(a):
    new_ary = []
    for i in range(len(a)):
        new_ary.append(a.pop(find_small_ele(a)))

    return new_ary


print(ary)
print(create_sort_ary(ary))
