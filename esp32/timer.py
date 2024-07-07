'''
接线说明：LED模块-->ESP32 IO
         (D1)-->(15)
         
D1指示灯间隔0.5s状态翻转
'''

from machine import Pin
from machine import Timer

class LedBlinkingController:
    def __init__(self, led_pin):
        # 初始化LED控制对象
        self.led = Pin(led_pin, Pin.OUT)
        self.led_state = 0  # 初始LED状态为关闭

        # 初始化定时器，设置为周期性触发，并绑定中断函数
        self.timer = Timer(0)
        self.timer.init(period=500, mode=Timer.PERIODIC, callback=self.timer_irq)
        self.led.value(self.led_state)  # 初始化LED状态

    def timer_irq(self, timer):
        # 定时器中断函数，翻转LED状态
        self.led_state = not self.led_state
        self.led.value(self.led_state)

    def run(self):
        # 程序主循环
        while True:
            pass  # 主循环中不需要执行任何操作，因为定时器中断会处理LED状态翻转

# 程序入口
if __name__ == "__main__":
    controller = LedBlinkingController(15)  # 假设LED连接到GPIO 15
    controller.run()
        
