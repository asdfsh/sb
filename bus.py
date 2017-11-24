# coding:utf-8

import copy
from datetime import datetime

def status_expansion(lines, max_stop):
    expanded_list = []
    cur_expanded = [[] for _ in range(0, max_stop)]
    prev_time = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        bus_num, arrived, nums, direction, stop, cur_time = line.split(',')
        stop = int(stop) - 1
        if prev_time is None:
            prev_time = cur_time

        if prev_time != cur_time:
            expanded_list.append((prev_time, cur_expanded))
            cur_expanded = [[] for i in range(0, max_stop)]
        prev_time = cur_time
        for _ in range(0, int(nums)):
            cur_expanded[stop].append(int(arrived))

    if prev_time:
        expanded_list.append((cur_time, cur_expanded))
    
    return expanded_list

def compute_augments(time, init_bus_status, max_stop):
    # 所有未到站车，让他们出发，方便计算路段时间
    augment_depart = [[] for i in range(0,max_stop)]
    # 所有到站车，让他们抵达，方便计算停留时间
    augment_arrival = [[] for i in range(0,max_stop)]
    # 处理第一波车
    for i in range(1, max_stop):
        for status in init_bus_status[i]:
            if status == 0:
                augment_depart[i-1].append(time)
            else:
                augment_arrival[i].append(time)
    return (augment_arrival, augment_depart)


def extract_time_expanded(expanded_list, max_stop):    
    arrives = [[] for i in range(0, max_stop)]
    departs = [[] for i in range(0, max_stop)]

    prev = [[] for i in range(0, max_stop)]
    for time, expanded in expanded_list:
        expanded_copy = copy.deepcopy(expanded)
        for i in range(0, max_stop):
            # 处理第一站, 如果有新车从第一站出现
            if i == 1 and expanded[i]:
                new_delta = expanded[i].count(0) - prev[i].count(0)
                for _ in range(0, new_delta):
                    departs[0].append(time)
            if prev[i]:
                prev[i].sort()
                # 处理最后一站
                if i == max_stop - 1:
                    last_stop_delta = len(prev[i]) - len(expanded_copy[i])
                    if last_stop_delta > 0: # 有车消失
                        for _ in range(0, last_stop_delta):
                            arrives[i].append(time)
                        continue
                for arrive_status in prev[i]:
                    # check if we've changed status or no
                    if arrive_status in expanded_copy[i]:
                        expanded_copy[i].remove(arrive_status)
                        continue
                    # bus hasn't arrived yet 
                    if arrive_status == 0:
                        # if it arrived
                        if 1 in expanded_copy[i]:
                            arrives[i].append(time)
                            expanded_copy[i].remove(1) 
                        # jumped a stop
                        # TODO: fix bus reaching final stop
                        elif i+1 < max_stop and 0 in expanded_copy[i+1]:
                            arrives[i].append(time)
                            departs[i].append(time)
                            expanded_copy[i+1].remove(0)
                    # bus arrived
                    if arrive_status == 1:
                        # check if it departed
                        # TODO: fix bus reaching final stop
                        if i+1 < max_stop and 0 in expanded_copy[i+1]:
                            departs[i].append(time)
                            expanded_copy[i+1].remove(0)
        prev = expanded

    return arrives, departs

# This is for testing...(need to change tests)
def extract_time(lines, max_stop):
    expanded = status_expansion(lines, max_stop)
    return extract_time_expanded(expanded, max_stop)

def get_time_diff(t1, t2):
    TIME = '%Y-%m-%d %H:%M:%S'
    diff = datetime.strptime(t2, TIME) - datetime.strptime(t1, TIME)
    return diff.seconds

def process_time(arrives, departs, max_stop):
    times = [[] for _ in range(0, max_stop)]
    for i in range(0, max_stop-1):
        for arrive_next, depart in zip(arrives[i+1], departs[i]):
            times[i].append(get_time_diff(depart, arrive_next))
    return times

def stay_time(arrives, departs, max_stop):
    stimes = [[] for _ in range(0, max_stop)]
    for i in range(0, max_stop):
        for arrive, depart in zip(arrives[i], departs[i]):
            stimes[i].append(get_time_diff(arrive, depart))
    return stimes

def extract_time_all(lines, max_stop):
    expanded = status_expansion(lines, max_stop)
    time, init_bus_status = expanded[0]
    arrive_aug, depart_aug = compute_augments(time, init_bus_status, max_stop)
    arrives, departs = extract_time_expanded(expanded, max_stop)
    arrives_copy = copy.deepcopy(arrives)
    departs_copy = copy.deepcopy(departs)

    # 计算路段时间时，添加初始离站信息
    for i in range(0, max_stop):
        if depart_aug[i]:
            depart_aug[i].extend(departs_copy[i])
            departs_copy[i] = depart_aug[i]
    ptime = process_time(arrives, departs_copy, max_stop)

    for i in range(0, max_stop):
        if arrive_aug[i]:
            arrive_aug[i].extend(arrives_copy[i])
            arrives_copy[i] = arrive_aug[i] 
    stime = stay_time(arrives_copy, departs, max_stop)
   
    return (ptime, stime)


if __name__ == '__main__':
    lines = []
    with open('buslian3.txt') as f:
        lines = f.readlines()
    max_stop = 6
    ptime, stime = extract_time_all(lines, max_stop)

    for i in range(0, max_stop ):
        print "process %d - %s" % (i+1,i+2)
        print ptime[i]
    for i in range(0, max_stop ):
        print "terminal %d" % (i+1)
        print stime[i]
