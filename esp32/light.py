from machine import Pin, Timer
from neopixel import NeoPixel
from simple import MQTTClient
import time
import network

#定义RGB控制对象
#控制引脚为16，RGB灯串联5个
pin=15
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)  

#定义RGB颜色
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
BLACK = (0, 0, 0)

COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

def RGB_led_off():
    for i in range(rgb_num):
        rgb_led[i]=(0, 0, 0)
        rgb_led.write()

def RGB_led_on():
    for color in COLORS:
        for i in range(rgb_num):
            rgb_led[i]=(color[0], color[1], color[2])
            rgb_led.write()
            time.sleep_ms(100)
        time.sleep_ms(1000)

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

class SmartBulb:
    def __init__(self, product_key, device_name, color='white', brightness=0, power_status='off'):
        self.product_key = product_key
        self.device_name = device_name
        self.color = color
        self.brightness = brightness
        self.power_status = power_status
        self.wifi = None
        self.bluetooth = None

    #开灯    
    def turn_on(self):        
        self.power_status = 'on'
        print(f"The bulb is now {self.color} and {self.brightness}% bright.")
    
    #关灯
    def turn_off(self):        
        self.power_status = 'off'
        print("The bulb is now off.")

    def set_color(self, color):
        if color in ['white', 'red', 'green', 'blue']:
            self.color = color
            print(f"The bulb color has been set to {self.color}.")
        else:
            print("Invalid color. Please choose from 'white', 'red', 'green', 'blue'.")

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness
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
        return {
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

    # 设备注册
    def iot_client.create_device(self, device_info):
        response = "ok. this is result of device_create"
        return  response
        
    # 设备状态上报
    def iot_client.update_device_status(status_info):
        response = "ok. update_device_status"
        return  response
 

# 使用示例
smart_bulb = SmartBulb(product_key="a1B2c3D4", device_name="SmartBulb001")
smart_bulb.turn_on()
smart_bulb.set_color("red")
smart_bulb.set_brightness(70)
smart_bulb.set_wifi("SSID_123")
smart_bulb.set_bluetooth(True)

# 获取当前状态
status = smart_bulb.get_status()
print(status)