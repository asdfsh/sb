# coding:utf-8

import copy
from datetime import datetime

def extract_time(lines, max_stop):    
    expanded_list = []
    cur_expanded = [[] for _ in range(0, max_stop)]
    prev_time = None
    arrives = [[] for i in range(0, max_stop)]
    departs = [[] for i in range(0, max_stop)]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        bus_num, arrived, nums, direction, stop, cur_time = line.split(',')
        stop = int(stop) - 1
        if prev_time is None:
            prev_time = cur_time
            initial_time=cur_time

        if cur_time == initial_time:
            for _ in range(0, int(nums)):
                if int(arrived) == 1:
                    arrives[stop].append(cur_time) 
                else:
                    if stop-1 >= 0:
                        departs[stop-1].append(cur_time)
        if prev_time != cur_time:
            expanded_list.append((prev_time, cur_expanded))
            cur_expanded = [[] for i in range(0, max_stop)]
        prev_time = cur_time
        for _ in range(0, int(nums)):
            cur_expanded[stop].append(int(arrived))

    if prev_time:
        expanded_list.append((cur_time, cur_expanded))

    prev = [None for i in range(0, max_stop)]
    for time, expanded in expanded_list:
        expanded_copy = copy.deepcopy(expanded)
        for i in range(0, max_stop):
            if prev[i]:
                prev[i].sort()
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

def get_time_diff(t1, t2):
    TIME = '%Y-%m-%d %H:%M:%S'
    diff = datetime.strptime(t2, TIME) - datetime.strptime(t1, TIME)
    return diff.seconds

def process_time(arrives, departs):
    times = [[] for _ in range(0, max_stop)]
    for i in range(0, max_stop-1):
        for arrive_next, depart in zip(arrives[i+1], departs[i]):
            times[i].append(get_time_diff(depart, arrive_next))
    return times

def stay_time(arrives, departs):
    stimes = [[] for _ in range(0, max_stop)]
    for i in range(0, max_stop):
        for arrive, depart in zip(arrives[i], departs[i]):
            stimes[i].append(get_time_diff(arrive, depart))
    return stimes

if __name__ == '__main__':
    lines = []
    with open('buslian2.txt') as f:
        lines = f.readlines()
    max_stop = 5
    arrives, departs = extract_time(lines, max_stop)
    times = process_time(arrives,departs)
    stimes = stay_time(arrives,departs)
    print "arrive times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print arrives[i]

    print "depart times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print departs[i]

    print "process times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print times[i]

    print "stay times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print stimes[i]