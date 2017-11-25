# coding:utf-8

import unittest
import bus

class Tests(unittest.TestCase):
    def test_basic(self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47']

        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [], [], [], []])
        self.assertEqual(stime, [[], [15], [], [], []])

    def test_initial (self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:52:47']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [], [], [], []])
        self.assertEqual(stime, [[], [], [], [], []])
    #初始数据 到达信息为0 则是刚刚离开上一站initial
    def test_initial2 (self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:52:47']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [], [], [], []])
        self.assertEqual(stime, [[], [], [], [], []])

    def test_final(self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:52:57', ]
        ptime, stime = bus.extract_time_all(lines, 3)
        self.assertEqual(ptime, [[], [10], []])
        self.assertEqual(stime, [[], [], []])

    def test_far(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,3,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:52:47']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [], [], [], []])
        self.assertEqual(stime, [[], [], [15], [], []])
    def test_stay(self):
            lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                     '801,1,1,0,1,2017-11-03 15:52:47',
                     '801,0,1,0,2,2017-11-03 15:53:02',
                     '801,1,1,0,2,2017-11-03 15:53:17',
                     '801,1,1,0,2,2017-11-03 15:53:32',
                     '801,0,1,0,3,2017-11-03 15:53:47',
                     ]

            ptime, stime = bus.extract_time_all(lines, 5)
            self.assertEqual(ptime, [[15], [], [], [], []])
            self.assertEqual(stime, [[], [30], [], [], []])

    def test_basic2(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,2,2017-11-03 15:53:02',
                 '801,1,1,0,2,2017-11-03 15:53:17']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[30], [], [], [], []])
        self.assertEqual(stime, [[], [], [], [], []])

    def test_not_arrived(self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:53:17'
                 ]
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[15], [30], [], [], []])
        self.assertEqual(stime, [[], [0], [], [], []])

    def test_not_process(self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:32',
                 '801,1,1,0,3,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:53:02',]
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [15], [], [], []])
        self.assertEqual(stime, [[], [0], [15], [], []])
        #考虑这种情况 并再写一个text
    def test_not_process2(self):
        lines = ['801,0,1,0,3,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:53:00',
                 '801,1,1,0,4,2017-11-03 15:53:17',
                 '801,0,1,0,5,2017-11-03 15:53:27',]
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[], [28], [17], [], []])
        self.assertEqual(stime, [[], [], [0], [10], []])
        #考虑没有过程时间且与其他数据混合

    def test_not_two_ex(self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:53:00',
                 '801,1,1,0,4,2017-11-03 15:53:17',
                 '801,0,1,0,5,2017-11-03 15:53:27', ]
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[15], [13], [17], [], []])
        self.assertEqual(stime, [[], [0], [0], [10], []])
        #考虑没有过程时间和没有停留时间混合
    def test_xx(self):
        print 'test xx'
        lines = ['801,0,2,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:53:02',
                 '801,0,1,0,3,2017-11-03 15:53:02']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[15,30], [], [], [], []])
        self.assertEqual(stime, [[], [15], [], [], []])


    def test_xxx(self):
        print 'test xxx'
        lines = ['801,0,3,0,2,2017-11-03 15:52:32',
                 '801,0,2,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,2,0,2,2017-11-03 15:53:02',
                 '801,0,1,0,3,2017-11-03 15:53:02',
                 ]
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[15, 30,30], [], [], [], []])
        self.assertEqual(stime, [[], [15], [], [], []])


    def test_xx2(self):
        print 'test xx2'
        lines = ['801,0,2,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,2,0,2,2017-11-03 15:53:02',
                 '801,1,1,0,2,2017-11-03 15:53:17',
                 '801,0,1,0,3,2017-11-03 15:53:17',
                 '801,0,2,0,3,2017-11-03 15:53:32']
        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[15, 30], [], [], [], []])
        self.assertEqual(stime, [[], [30,30], [], [], []])


    def test_multistart(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,3,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:52:47',
                 '801,1,1,0,2,2017-11-03 15:53:00',
                 '801,1,1,0,4,2017-11-03 15:53:00',
                 '801,0,1,0,3,2017-11-03 15:53:10',
                 '801,0,1,0,5,2017-11-03 15:53:10',
                 '801,1,1,0,3,2017-11-03 15:53:17',
                 '801,1,1,0,5,2017-11-03 15:53:17']

        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[13],[7],[13],[7],[]])
        self.assertEqual(stime, [[],[10],[15],[10],[]])

    def test_newbus(self):
        lines = [
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:52:47',
                 '801,0,1,0,2,2017-11-03 15:53:00',#00秒出发一辆新车
                 '801,1,1,0,3,2017-11-03 15:53:00',
                 '801,1,1,0,4,2017-11-03 15:53:00',
                 '801,1,1,0,2,2017-11-03 15:53:08',
                 '801,0,1,0,4,2017-11-03 15:53:10',
                 '801,0,1,0,5,2017-11-03 15:53:10',
                ]

        ptime, stime = bus.extract_time_all(lines, 5)
        self.assertEqual(ptime, [[8],[13],[13],[],[]])
        self.assertEqual(stime, [[],[],[],[],[]])
        #新车应该有第一站到第二站的ptime

if __name__ == '__main__':
    unittest.main()