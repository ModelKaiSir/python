'''
    贪婪算法
'''


# 包含需要覆盖的州的列表,用集合表示,不包含重复元素
states_needed = set(["mt", "wa", "or", "id", "nv", "ut", "ca", "az"])
# 可供选择的广播台清单,用散列表表示
stations = {}
stations["kfour"] = set(["nv","ut"])
stations["qiukai"] = set(["b","a"])
stations["kfive"] = set(["ca","az","or"])
stations["kone"] = set(["id","nv","ut"])
stations["ktwo"] = set(["wa","id","mt"])
stations["kthree"] = set(["or","nv","ca"])


print(stations)

final_stations = set()

while states_needed:
    best_station = None

    states_covered = set()
    print("start")
    for station, states in stations.items():
        print("台 {}".format(station))
        covered = states_needed & states
        print("当前台覆盖的州和需要覆盖的州中重复的台 {}".format(covered))
        # 找寻最优解 当前问题中要找符合条件的 （在 州中 存在符合条件的台）
        # 最优解为 不但符合条件 还比其他州的台多
        if covered != set():
            if len(covered) > len(states_covered):

                print("重复的台比上一个包含的states_covered多的时候优于上一个解")
                best_station = station
                print("上次states_covered为 {}".format(states_covered))
                states_covered = covered
                print("更新states_covered {}".format(states_covered))
                final_stations.add(best_station)
        else:
            print("在{}中没有找到符合条件的台".format(station))
    states_needed -= states_covered
    print("还没覆盖的州 {}".format(states_needed))


print(final_stations)
