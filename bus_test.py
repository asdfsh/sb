import unittest
# coding:utf-8
import bus

class Tests(unittest.TestCase):
    def test_basic(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],[],[]])
        self.assertEqual(departs, [[],['2017-11-03 15:52:47'],[],[]])

    def test_initial (self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],[],[]])
        self.assertEqual(departs, [[],[],['2017-11-03 15:52:47'],['2017-11-03 15:52:47']])
    #初始数据 到达信息为0 则是刚刚离开上一站initial
    def test_initial2 (self):
        lines = ['801,1,1,0,2,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],['2017-11-03 15:52:47'],['2017-11-03 15:52:47']])
        self.assertEqual(departs, [[],[],[],[]])

    def test_far(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,3,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,4,2017-11-03 15:52:47']
        arrives, departs = bus.extract_time(lines,4)
        self.assertEqual(arrives, [[],[],[],[],[]])
        self.assertEqual(departs, [[],['2017-11-03 15:52:47'],[],['2017-11-03 15:52:47'],[]])
    def test_stay(self):
            lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                     '801,1,1,0,1,2017-11-03 15:52:47',
                     '801,0,1,0,2,2017-11-03 15:53:02',
                     '801,1,1,0,2,2017-11-03 15:53:17',
                     '801,1,1,0,2,2017-11-03 15:53:32',
                     '801,0,1,0,3,2017-11-03 15:53:47',
                     ]
            arrives, departs = bus.extract_time(lines, 3)
            self.assertEqual(arrives, [[], [], ['2017-11-03 15:53:17'], []])
            self.assertEqual(departs, [[], ['2017-11-03 15:53:02'], ['2017-11-03 15:53:47'], []])

    def test_basic2(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,2,2017-11-03 15:53:02',
                 '801,1,1,0,2,2017-11-03 15:53:17']
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],['2017-11-03 15:53:17'],[]])
        self.assertEqual(departs, [[],['2017-11-03 15:52:47'],[],[]])

    def test_not_arrived(self):
        lines = ['801,0,1,0,2,2017-11-03 15:52:32',
                 '801,0,1,0,3,2017-11-03 15:52:47',
                 '801,1,1,0,3,2017-11-03 15:53:17'
                 ]
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],['2017-11-03 15:52:47'],['2017-11-03 15:53:17']])
        self.assertEqual(departs, [[],[],['2017-11-03 15:52:47'],[]])

    def test_not_process(self):
        lines = ['801,1,1,0,1,2017-11-03 15:52:32',
                 '801,1,1,0,2,2017-11-03 15:52:47',
                 '801,0,1,0,3,2017-11-03 15:53:02',]
        arrives, departs = bus.extract_time(lines,3)
        self.assertEqual(arrives, [[],[],['2017-11-03 15:52:47'],[]])
        self.assertEqual(departs, [[],['2017-11-03 15:52:47'],['2017-11-03 15:53:02'],[]])

    def test_xx(self):
        print 'test xx'
        lines = ['801,0,2,0,1,2017-11-03 15:52:32',
                 '801,0,1,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:52:47',
                 '801,1,1,0,1,2017-11-03 15:53:02',
                 '801,0,1,0,2,2017-11-03 15:53:02']
        arrives, departs = bus.extract_time(lines, 3)
        self.assertEqual(arrives, [[], ['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [[], ['2017-11-03 15:53:02'], [], []])

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
        self.assertEqual(arrives, [[], ['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [[], ['2017-11-03 15:53:02'], [], []])

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
        self.assertEqual(arrives, [[], ['2017-11-03 15:52:47', '2017-11-03 15:53:02'], [], []])
        self.assertEqual(departs, [[], ['2017-11-03 15:53:17','2017-11-03 15:53:32'], [], []])

if __name__ == '__main__':
    unittest.main()