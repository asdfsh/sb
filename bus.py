import copy
from datetime import datetime
def extract_time(lines, max_stop):    
    expanded_list = []
    cur_expanded = [ [] for i in range(0, max_stop+1)]
    prev_time = None

    arrives = [[] for i in range(0, max_stop + 1)]
    departs = [[] for i in range(0, max_stop + 1)]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        NO, arrived, nums, direction, stop, cur_time = line.split(',')



        if prev_time is None:
            prev_time = cur_time
            initial_time=cur_time

        if cur_time == initial_time:
            for _ in range(0, int(nums)):
              if int(arrived) == 1:
                arrives[int(stop)].append(cur_time)
              else:
                departs[int(stop)-1].append(cur_time)
        if prev_time != cur_time:
            expanded_list.append(cur_expanded)
            cur_expanded = [[] for i in range(0, max_stop+1)]
        prev_time = cur_time
        for i in range(0, int(nums)):
            cur_expanded[int(stop)].append(int(arrived))
            cur_expanded[0] = cur_time

    if prev_time:
        expanded_list.append(cur_expanded)


    # TODO: should adjust prev based on expanded_list[0]
    prev = [None for i in range(0, max_stop+1)]
    for expanded in expanded_list:
        expanded_copy = copy.deepcopy(expanded)
        for i in range(1, max_stop+1):


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
                            arrives[i].append(expanded[0])
                            expanded_copy[i].remove(1) 
                        # jumped a stop
                        # TODO: fix bus reaching final stop
                        elif i+1<=max_stop and 0 in expanded_copy[i+1]:
                            arrives[i].append(expanded[0])
                            departs[i].append(expanded[0])
                            expanded_copy[i+1].remove(0)
                    # bus arrived
                    if arrive_status == 1:
                        # check if it departed
                        # TODO: fix bus reaching final stop
                        if i+1<=max_stop and 0 in expanded_copy[i+1]:
                            departs[i].append(expanded[0])
                            expanded_copy[i+1].remove(0)
        prev = expanded

    return arrives, departs
def process_time(arrives,departs):
    times = [[] for i in range(0, max_stop + 1)]
    for i in range(0, max_stop):
        for arrive, depart in zip(arrives[i+1], departs[i]):
            TIME = '%Y-%m-%d %H:%M:%S'
            a =datetime.strptime(arrive,TIME)-datetime.strptime(depart,TIME)
            time=a.seconds
            times[i].append(time)
    return times
if __name__ == '__main__':
    lines = []
    with open('buslian2.txt') as f:
        lines = f.readlines()
    max_stop = 7
    arrives, departs = extract_time(lines, max_stop)
    times=process_time(arrives,departs)
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
