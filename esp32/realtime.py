'''
接线说明：DS1302时钟模块-->ESP32 IO
         (CE)-->(23)
         (IO)-->(19)
         (CK)-->(18)
         
软件shell控制台间隔1S输出DS1302实时时钟年月日时分秒星期
'''

#导入Pin模块
from machine import Pin
import time
import DS1302

#定义DS1302控制对象
ds1302=DS1302.DS1302(clk=Pin(18),dio=Pin(19),cs=Pin(23))

#定义星期
week=("星期一","星期二","星期三","星期四","星期五","星期六","星期天")

#程序入口
if __name__=="__main__":
    if ds1302.DateTime()[0]!=2024:
        ds1302.DateTime([2024,7,10, 2, 21,18,58])  #年-月-日 星期 时：分：秒 微秒 （其中星期：0~6示周一~日）
    while True:
        date_time=ds1302.DateTime()
        print("%d-%d-%d \t %02d:%02d:%02d \t %s" %(date_time[0],date_time[1],date_time[2],
                                                   date_time[4],date_time[5],date_time[6],
                                                   week[date_time[3]]))
        time.sleep(1)
        