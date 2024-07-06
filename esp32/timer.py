'''
接线说明：LED模块-->ESP32 IO
         (D1)-->(15)
         
D1指示灯间隔0.5s状态翻转
'''

#导入Pin模块
from machine import Pin
from machine import Timer

#定义LED控制对象
led1=Pin(15,Pin.OUT)


#定义LED状态
led1_state=0

#定时器0中断函数
def time0_irq(time0):
    global led1_state
    led1_state=not led1_state
    led1.value(led1_state)
        
#程序入口
if __name__=="__main__":
    led1.value(led1_state)  #初始化LED，熄灭状态
    
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=500,mode=Timer.PERIODIC,callback=time0_irq)
    
    while True:
        pass
