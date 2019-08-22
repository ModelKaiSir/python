import random
import itertools

# 投掷600次2颗骰子
roll_value = [a+b for a, b in zip([random.randint(1, 6) for i in range(600)], [random.randint(1, 6) for i in range(600)])]
print(roll_value)
# 统计每个值出现的次数
roll_val = [roll_value.count(i) for i in range(12)]
print(roll_val)


