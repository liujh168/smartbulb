'''
接线说明：蜂鸣器模块-->ESP32 IO
         (BEEP)-->(25)
'''

from machine import Pin
import time

BPIO_BEEP=25
TIME_BEEP=5  #响几秒

class Beep:
    def __init__(self, pin):
        self.beep = Pin(pin, Pin.OUT)  # 创建蜂鸣器控制对象
        self.count=0

    def beep_on(self):
        i = 1  
        while self.count < TIME_BEEP*2000:  #约5秒
            i = not i  
            self.beep.value(i)  
            time.sleep_us(250)  # 脉冲频率为 2KHz
            self.count = self.count + 1

    def beep_off(self):
        self.status="off"
        

#测试程序入口
if __name__=="__main__":
    beep = Beep(BPIO_BEEP)  # 实例化 Beep 类，并指定连接蜂鸣器的引脚
    beep.beep_on()  # 启动蜂鸣器发声
