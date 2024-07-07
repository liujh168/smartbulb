from machine import Pin

class Beep:
    def __init__(self, pin):
        self.beep = Pin(pin, Pin.OUT)  # 创建蜂鸣器控制对象

    def beep_on(self):
        i = 1  
        while True:
            i = not i  
            self.beep.value(i)  
            time.sleep_us(250)  # 脉冲频率为 2KHz

#测试程序入口
if __name__=="__main__":
    beep = Beep(25)  # 实例化 Beep 类，并指定连接蜂鸣器的引脚
    beep.beep_on()  # 启动蜂鸣器发声
