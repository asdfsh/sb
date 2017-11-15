# coding:utf-8

import unittest
import bus

class Tests(unittest.TestCase):
    def test_basic(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [['2017-11-03 15:52:32'],[],[]])
        self.assertEqual(departs, [['2017-11-03 15:52:47'],[],[]])

    def test_initial (self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],[]])
        self.assertEqual(departs, [['2017-11-03 15:52:47'],['2017-11-03 15:52:47'],[]])
    #初始数据 到达信息为0 则是刚刚离开上一站initial
    def test_initial2 (self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],['2017-11-03 15:52:47'],['2017-11-03 15:52:47']])
        self.assertEqual(departs, [[],[],[]])

    def test_final(self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:52:57', ]
        arrives, departs = bus.extract_time(lines, 3)
        self.assertEqual(arrives, [[], ['2017-11-03 15:52:47'], ['2017-11-03 15:52:57']])
        self.assertEqual(departs, [[], ['2017-11-03 15:52:47'], []])
    #假设第三站是最后一站，而47秒是公交消失前的最后一条记录，所以公交57秒假设公交恰好到终点站，此时公交消失,还没实现？
    def test_far(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,3,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,4)
        self.assertEqual(arrives, [['2017-11-03 15:52:32'],[],['2017-11-03 15:52:32'],[]])
        self.assertEqual(departs, [['2017-11-03 15:52:47'],[],['2017-11-03 15:52:47'],[]])
    def test_stay(self):
            lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                     '801,1,1,0,1,2017-11-03 15:52:47',
                     '801,0,1,0,2,2017-11-03 15:53:02',
                     '801,1,1,0,2,2017-11-03 15:53:17',
                     '801,1,1,0,2,2017-11-03 15:53:32',
                     '801,0,1,0,3,2017-11-03 15:53:47',
                     ]
            arrives, departs = bus.extract_time(lines, 3)
            self.assertEqual(arrives, [['2017-11-03 15:52:32'], ['2017-11-03 15:53:17'], []])
            self.assertEqual(departs, [['2017-11-03 15:53:02'], ['2017-11-03 15:53:47'], []])

    def test_basic2(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,2,2017-11-03 15:53:02',
                 '801,1,1,0,2,2017-11-03 15:53:17']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [['2017-11-03 15:52:32'],['2017-11-03 15:53:17'],[]])
        self.assertEqual(departs, [['2017-11-03 15:52:47'],[],[]])

    def test_not_arrived(self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:53:17'
                 ]
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],['2017-11-03 15:52:47'],['2017-11-03 15:53:17']])
        self.assertEqual(departs, [['2017-11-03 15:52:32'],['2017-11-03 15:52:47'],[]])

    def test_not_process(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:53:02',]
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [['2017-11-03 15:52:32'],['2017-11-03 15:52:47'],[]])
        self.assertEqual(departs, [['2017-11-03 15:52:47'],['2017-11-03 15:53:02'],[]])
        #暂不考虑这种情况

    def test_xx(self):
        print 'test xx'
        lines = ['801,0,2,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:53:02',
                 '801,0,1,0,2,2017-11-03 15:53:02']
        arrives, departs = bus.extract_time(lines, 3)
        self.assertEqual(arrives, [['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [['2017-11-03 15:53:02'], [], []])
        #有两辆车的时候 程序运行只有一个depart时间

    def test_xxx(self):
        print 'test xxx'
        lines = ['801,0,3,0,1,2017-11-03 15:52:32',
                 '801,0,2,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:52:47',
                 '801,0,1,0,1,2017-11-03 15:53:02',
                 '801,1,1,0,1,2017-11-03 15:53:02',
                 '801,0,1,0,2,2017-11-03 15:53:02',
                 ]
        arrives, departs = bus.extract_time(lines, 3)
        self.assertEqual(arrives, [['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [['2017-11-03 15:53:02'], [], []])

    # 三辆车同理 程序运行只有一个depart时间
    def test_xx2(self):
        print 'test xx2'
        lines = ['801,0,2,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:52:47',
                 '801,1,2,0,1,2017-11-03 15:53:02',
                 '801,1,1,0,1,2017-11-03 15:53:17',
                 '801,0,1,0,2,2017-11-03 15:53:17',
                 '801,0,2,0,2,2017-11-03 15:53:32']
        arrives, departs = bus.extract_time(lines, 3)
        self.assertEqual(arrives, [['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [['2017-11-03 15:53:17','2017-11-03 15:53:32'], [], []])
#有两辆车的时候 程序运行只有一个depart时间
if __name__ == '__main__':
    unittest.main()