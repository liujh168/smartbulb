'''
接线说明：数码管模块-->ESP32 IO
         CLK-->(16)
         DIO-->(17)
数码管间隔1s从0开始计数显示
'''
from machine import Pin
import time
import tm1637

class SegmentDisplayController:
    def __init__(self, clk_pin, dio_pin):
        # 初始化数码管控制对象
        self.smg = tm1637.TM1637(clk=Pin(clk_pin), dio=Pin(dio_pin))
        self.count = 0  # 计数器

    def display_count(self):
        # 显示当前计数器的值
        self.smg.number(self.count)
        #smg.numbers(1,24)  #显示小数01.24
        #smg.hex(123)  #将十进制数转换十六进制显示
        #smg.brightness(0)  #亮度调节
        #smg.temperature(25)  #显示带温度符号°C，整数温度值
        #smg.show("1314")  #字符串显示，显示整数
        #smg.scroll("1314-520",500)  #字符串滚动显示，速度调节
        #smg.number(n)

    def run(self):
        # 程序主循环
        while True:
            self.display_count()
            self.count += 1  # 计数器递增
            time.sleep(1)  # 间隔1秒更新显示

# 程序入口
if __name__ == "__main__":
    controller = SegmentDisplayController(16, 17)  # 假设CLK连接到GPIO 16，DIO连接到GPIO 17
    controller.run()
