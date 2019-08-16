import random

'''
    二分法查找元素
    左边界 右边界
    对列表内的元素（已排序的）进行 下标/2 与目标元素对比 大了左边界 = 当前下标+1 
    小了 右边界 = 当前下标 - 1
    等于即找到目标
'''


# 普通实现
def bad(ls, search_item):
    for i in ls:
        if i == search_item:
            print("找到" + str(i))
        else:
            continue

    print("done")


ls = range(999999)
pot = random.randrange(999999)
print(ls)
print(pot)


# bad(ls, pot)

# 二分法
def fine(ls, search_item):
    low, high = 0, len(ls) - 1

    while low <= high:
        print("low {} high {} ".format(low, high))
        mid = (low + high) // 2
        guess = ls[mid]
        print("中位数{}".format(mid))
        print("中位数的值{}".format(guess))
        print("输入的值{}".format(search_item))

        if guess > search_item:
            high = mid - 1
            print("{}>{}".format(guess, search_item))
        elif guess < search_item:
            low = mid + 1
            print("{}<{}".format(guess, search_item))
        else:
            print("low {} high {} guess {} ".format(low, high, guess))
            return None


# 二分法
def fine2(ls, search_item):
    low, high = 0, len(ls) - 1

    while low <= high:
        mid = (low + high) // 2
        if search_item == ls[mid]:
            return search_item
        elif search_item > ls[mid]:
            low = mid + 1
        else:
            high = mid - 1
    return None


fine(ls, pot)

# print(fine2(sorted(ls), pot))
