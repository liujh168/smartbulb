import time
from machine import Pin

def beep():
    #定义蜂鸣器控制对象
    beep=Pin(25,Pin.OUT)   
    i=0    
    while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_us(250)  #脉冲频率为2KHz

#测试程序入口
if __name__=="__main__":
    print("this is a test!")
    beep()

