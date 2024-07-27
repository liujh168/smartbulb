'''
接线说明：继电器模块-->ESP32 IO
         (REL)-->(25)
         继电器模块输出-->LED模块
         (COM)-->(3V3)
         (NO)-->(D1)
继电器模块间隔一定时间吸合断开，吸合时D1指示灯亮，断开时灭
'''

from machine import Pin
import time

class RelayController:
    def __init__(self, relay_pin):
        # 初始化继电器控制对象
        self.relay = Pin(relay_pin, Pin.OUT)
        self.led_state = False  # 初始LED状态为关闭

    def toggle_relay(self):
        # 切换继电器状态
        self.led_state = not self.led_state
        self.relay.value(self.led_state)

    def on(self):
        # 切换继电器状态
        self.led_state = 1
        self.relay.value(self.led_state)

    def off(self):
        # 切换继电器状态
        self.led_state = 0
        self.relay.value(self.led_state)

# 程序入口
if __name__ == "__main__":
    controller = RelayController(25)  # 假设继电器模块连接到GPIO 25
    # 程序主循环
    while True:
        controller.toggle_relay()
        time.sleep(1)  # 间隔一定时间切换继电器状态
        controller.toggle_relay()
        time.sleep(3)  # 间隔一定时间切换继电器状态


