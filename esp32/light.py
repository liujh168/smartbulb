from machine import Pin
from neopixel import NeoPixel
import time

#产品和设备信息：schema和profile字典定义了智能灯泡的属性、控制命令和配置信息。
#产品类型...
schema = {
  "productKey": "a1B2c3D4",
  "deviceName": "SmartBulb001",
  "attributes": {
    "color": {
      "type": "string",
      "enum": ["white", "red", "green", "blue"]
    },
    "brightness": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
    },
    "powerStatus": {
      "type": "string",
      "enum": ["on", "off"]
    }
  },
  "controls": {
    "turnOn": {
      "type": "command"
    },
    "turnOff": {
      "type": "command"
    },
    "setColor": {
      "type": "command"
    }
  },
  "configurations": {
    "wifi": {
      "type": "string"
    },
    "bluetooth": {
      "type": "boolean"
    }
  }
}

#设备信息...
profile = {
  "productKey": "a1B2c3D4",
  "deviceName": "SmartBulb001",
  "attributes": {
    "color": "white",
    "brightness": 70,
    "powerStatus": "on"
  },
  "controls": {
    "turnOn": "Turn the bulb on",
    "turnOff": "Turn the bulb off",
    "setColor": "Set the color of the bulb"
  },
  "configurations": {
    "wifi": "SSID_123",
    "bluetooth": "ON"
  }
}

#定义了几种RGB颜色和颜色列表COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 150, 0)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
#COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)
COLORS = (RED, GREEN, BLUE)

led1 = Pin(5, Pin.OUT) # 定义LED对象，指示wifi连接状态

# rgb_num 定义RGB控制对象
# pin 控制引脚为16，RGB灯串联5个
class SmartBulb:
    def __init__(self, product_key, device_name, color='white', brightness=0, power_status='off', rgb_num=5, pin=15):
        self.product_key = product_key
        self.device_name = device_name
        self.color = color
        self.brightness = brightness
        self.power_status = power_status
        self.wifi = None
        self.bluetooth = None
        self.rgb_num = rgb_num
        self.pin = pin
        self.rgb_led = NeoPixel(Pin(pin,Pin.OUT),self.rgb_num)  

    def turn_on(self):
        led1.value(1)
        for color in COLORS:
            for i in range(self.rgb_num):
                self.rgb_led[i]=(color[0], color[1], color[2])
                self.rgb_led.write()
                time.sleep_ms(100)
            time.sleep_ms(1000)
        self.power_status = 'on'
        #self.set_color(self.color)
        #self.set_brightness(self.brightness)
        #print(f"The bulb is now {self.color} and {self.brightness}% bright.")

    def turn_off(self):
        led1.value(0)
        for i in range(self.rgb_num):
            self.rgb_led[i]=(0, 0, 0)
            self.rgb_led.write()
        self.power_status = 'off'
        #self.set_color(self.color)
        #self.set_brightness(self.brightness)
        #print("The bulb is now off.")

    def set_color(self, color):
        if color in ['white', 'red', 'green', 'blue']:
            self.color = color
            if self.color == "red":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(255, 0, 0)     #self.rgb_led[i]=(RED)
                    self.rgb_led.write()
                print(f"The bulb color has been set to {self.color}.")
            if self.color == "green":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(0, 255, 0)     #self.rgb_led[i]=(GREEN)
                    self.rgb_led.write()
                print(f"The bulb color has been set to {self.color}.")
            if self.color == "blue":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(0, 0, 255)     #self.rgb_led[i]=(BLUE)
                    self.rgb_led.write()
                print(f"The bulb color has been set to {self.color}.")
            if self.color == "white":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(WHITE)
                    self.rgb_led.write()
                print(f"The bulb color has been set to {self.color}.")
        else:
            print("Invalid color. Please choose from 'white', 'red', 'green', 'blue'.")

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness
            if self.color == "white":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(self.brightness, self.brightness, self.brightness)
                    self.rgb_led.write()
            print(f"The bulb brightness has been set to {self.brightness}%.")
            if self.color == "red":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(self.brightness, 0, 0)
                    self.rgb_led.write()
            print(f"The bulb brightness has been set to {self.brightness}%.")
            if self.color == "green":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(0, self.brightness, 0)
                    self.rgb_led.write()
            print(f"The bulb brightness has been set to {self.brightness}%.")
            if self.color == "blue":
                for i in range(self.rgb_num):
                    self.rgb_led[i]=(0, 0, self.brightness)
                    self.rgb_led.write()
            print(f"The bulb brightness has been set to {self.brightness}%.")
        else:
            print("Invalid brightness. Please enter a value between 0 and 100.")

    def set_wifi(self, ssid):
        self.wifi = ssid
        print(f"Wi-Fi has been set to {self.wifi}.")

    def set_bluetooth(self, enabled):
        if isinstance(enabled, bool):
            self.bluetooth = enabled
            print("Bluetooth has been turned " + ("on" if self.bluetooth else "off"))
        else:
            print("Invalid input for Bluetooth. Please use a boolean value.")
      
    def get_status(self):
        json_str = {
            'productKey': self.product_key,
            'deviceName': self.device_name,
            'attributes': {
                'color': self.color,
                'brightness': self.brightness,
                'powerStatus': self.power_status
            },
            'configurations': {
                'wifi': self.wifi,
                'bluetooth': self.bluetooth
            }
        }
        return  json_str

# 测试
if __name__ == "__main__":
    smart_bulb = SmartBulb(product_key="a1B2c3D4", device_name="SmartBulb001")
    print(smart_bulb)
    while True:
        print("以下获取灯的状态！ json串表示")
        status = smart_bulb.get_status()  
        print(status)
        time.sleep(3000)
        print("关灯！")
        smart_bulb.turn_off()
        print(profile["attributes"])
        print("RGB_LED 开灯了！")
        smart_bulb.turn_on()
        print(profile["attributes"])
        time.sleep(5000)


