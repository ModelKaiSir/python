import random
import itertools
import pygal

# 投掷600次2颗骰子 Pygal
roll_value = [a + b for a, b in
              zip([random.randint(1, 6) for i in range(600)], [random.randint(1, 6) for i in range(600)])]
# 统计每个值出现的次数
roll_val = range(12)
roll_val_count = [roll_value.count(i) for i in roll_val]

bar_chart = pygal.Bar()
bar_chart.title = "Roll Value Chart"
bar_chart.x_labels = map(str, roll_val)
bar_chart.add("Roll A", roll_val_count)
bar_chart.render_to_file("roll.svg")
