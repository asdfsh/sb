from pyExcelerator import *

# coding:utf-8
import requests
import time
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
w = Workbook()
ws = w.add_sheet('hk')
dir=0
file3=open('buslian1116.txt','w+')

fname = "busNO.xlsx"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("Sheet1")
    #sh = bk._sheet_name("Sheet1")
except:
    print "no sheet in %s named 2" % fname
nrows = sh.nrows
ncols = sh.ncols
#print "nrows %d, ncols %d" % (nrows,ncols)
cell_value = sh.cell_value(0,0)
#print cell_value
row_list = []
for i in range(0,nrows):
 row_data = sh.row_values(i)
 row_list.append(row_data)
#print int(row_list[2][0])

nums={'1':'522',
      '2':'552'
               }
# 10 1h=360 2h=720 4h=1440 8h=2880
# 15 1h=540 2h=1080 4h=2160 8h=4320
for j in range(0,4320):

 #print "Start : %s" % time.ctime()
 #file3.write(time.ctime()+'\n')
  for i in range(0,8):

   data={'Type': 'LineDetail', 'lineNo': '%s'% int(row_list[i][0]), 'direction': 0}
   try:
    a=requests.post("http://www.wbus.cn/getQueryServlet", data)
   except:
       a=a
  #print a
  #print a.json()
   try:
      data = a.json()
   except:
        data=data
  #file3.write(str(int(row_list[i][1]))+'\n')
   for bus in data['data']['bus']:
    scode=bus['order']*2+bus['arrived']-3
    #print int(row_list[i][0]) ,bus['arrived'], bus['busNum'], dir, bus['order'],data['data']['stops'][bus['order']-1]['stopName'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print scode,bus['order'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    file3.write(str(int(row_list[i][0]))+','+str(bus['arrived'])+','+str(bus['busNum'])+','+str(dir)+','+str(bus['order'])+','+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')#txt

    # print bus
  #for a in range (0,15):

    #ws.write(a,0,'haha')
#w.save('a.xlsx')
#/ wanttosave in excel
  time.sleep(15)
  file3.write('\n')
file3.close() #txt
#ws.write(1,0,'haha')
#w.save('b.xls')