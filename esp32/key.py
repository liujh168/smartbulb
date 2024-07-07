from machine import Pin
import time

class ButtonLedController:
    def __init__(self):
        # 初始化按键和LED的GPIO
        self.keys = {
            'K1': Pin(14, Pin.IN, Pin.PULL_UP),
            'K2': Pin(27, Pin.IN, Pin.PULL_UP),
            'K3': Pin(26, Pin.IN, Pin.PULL_UP),
            'K4': Pin(25, Pin.IN, Pin.PULL_UP)
        }
        self.leds = {
            'D1': Pin(15, Pin.OUT),
            'D2': Pin(2, Pin.OUT),
            'D3': Pin(0, Pin.OUT),
            'D4': Pin(4, Pin.OUT)
        }
        self.key_press = 0  # 初始按键状态
        self.led_states = {key: 0 for key in self.leds}  # 初始化LED状态

    def key_scan(self):
        # 按键扫描函数
        if self.key_press == 1 and any(not key.value() for key in self.keys.values()):
            time.sleep_ms(10)  # 消抖
            self.key_press = 0
            for key_name, key in self.keys.items():
                if not key.value():
                    return key_name
        elif all(key.value() for key in self.keys.values()):
            self.key_press = 1
        return None

    def control_led(self, key_press):
        # 根据按键控制对应的LED
        if key_press:
            led_name = 'D' + key_press[1]  # 按键K1-K4对应D1-D4
            self.led_states[led_name] = not self.led_states[led_name]
            self.leds[led_name].value(self.led_states[led_name])

    def run(self):
        # 程序主循环
        while True:
            key_press = self.key_scan()
            if key_press:
                self.control_led(key_press)

# 程序入口
if __name__ == "__main__":
    controller = ButtonLedController()
    controller.run()