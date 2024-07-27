from machine import Pin, Timer
from neopixel import NeoPixel
from simple import MQTTClient
import json
import time
import network
from timer import   TimerRelay
from relay import RelayController

#设备信息...
status_info = {
  "productKey": "a1B2c3D4",
  "deviceName": "SmartBulb001",
  "attributes": {
    "color": "white",
    "brightness": 70,
    "powerStatus": "off"
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
relay = RelayController(25)
 
def RGB_led_on():
    relay.on()
    for color in COLORS:
        for i in range(rgb_num):
            rgb_led[i]=(color[0], color[1], color[2])
            rgb_led.write()
            time.sleep_ms(100)
        time.sleep_ms(1000)

def RGB_led_off():
    relay.off()
    for i in range(rgb_num):
        rgb_led[i]=(0, 0, 0)
        rgb_led.write()

def RGB_led_status():
    powerstatus = status_info["attributes"]["powerStatus"]
    brightness = status_info["attributes"]["brightness"]
    color = status_info["attributes"]["color"]

    # 正确创建字典，并使用字符串作为键
    json_status = {
        'status': 'RGB_light is online',
        'Powerstatus': powerstatus,
        'Brightness': brightness,
        'Color': color
    }

    # 将字典转换为JSON字符串，如果需要的话
    json_status_str = json.dumps(json_status)

    return json_status_str

# WIFI连接函数
def wifi_connect(ssid, password, retries=5, delay=15):  # Wi-Fi连接函数
    led1 = Pin(5, Pin.OUT) # 定义LED对象，指示wifi连接状态
    wlan = network.WLAN(network.STA_IF)  # STA模式
    wlan.active(True)  # 激活网络接口
    start_time = time.time()  # 记录开始连接的时间

    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(ssid, password)  # 连接到指定WIFI
        while not wlan.isconnected():
            led1.value(1)  # LED闪烁表示正在尝试连接
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(300)
            
            # 超过15秒未连接成功，视为超时
            if time.time() - start_time > delay:
                print("WIFI Connect Timeout!")
                led1.value(0)  # 超时后关闭LED
                return False
            
    led1.value(1)  # LED常亮
    print("Network connected!")
    print("Network information:", wlan.ifconfig())
    return True

#以下MQTT相关
# 配置信息
CONFIG = {
    "ssid": "liujh",
    "password": "56865686",
    "mqtt_server": "120.26.241.36",
    "mqtt_port": 1083,
    "client_id": "ESP32_Client",
    "topic": "mytest",
    "mqtt_broker_username": "ljh",
    "mqtt_broker_password": "56865686"
}

#设置 MQTT 回调函数,有信息时候执行
def mqtt_callback(topic,msg):
    message_str = msg.decode('utf-8')  # 将字节类型的消息解码为字符串
    print(f"Received message from topic {topic}: {message_str}")
    if message_str == "on":  
        print("以下打开灯光！")
        RGB_led_on()
        status_info["attributes"]["powerStatus"]="on"
        #报告一下状态
        client.publish(CONFIG['topic'], "poweron")
        
    if message_str == "off":  
        RGB_led_off()
        status_info["attributes"]["powerStatus"]="off"
        #报告一下状态
        print("彩灯已关闭！")
        client.publish(CONFIG['topic'], "poweroff")
        
    if message_str == "status":
        print("问灯的状态呢？")
        json_status =  RGB_led_status()
        print(json_status)
        client.publish(CONFIG['topic'], "RGB light status:........... ")
        client.publish(CONFIG['topic'], json_status)

    # 设备注册
    #def iot_client.create_device(self, device_info):
    #    response = "ok. this is result of device_create"
    #    return  response
        
    # 设备状态上报
    #def iot_client.update_device_status(status_info):
    #    response = "ok. update_device_status"
    #    return  response

# 主程序
if __name__ == "__main__":
    msg = ""
    msg_count=0

    #controller = TimerRelay(25)  # 假设LED连接到GPIO 15            

    if wifi_connect(CONFIG['ssid'], CONFIG['password']):
        try:
            SERVER="120.26.241.36"
            PORT=1083
            CLIENT_ID="ESP32_Client"  #客户端ID
            TOPIC="mytest/#"  #TOPIC名称
            client = MQTTClient(CLIENT_ID, SERVER, PORT, "ljh", "56865686")  #建立客户端
            #client = MQTTClient(CONFIG['client_id'], CONFIG['mqtt_server'], CONFIG['mqtt_port'],
            #                    CONFIG['mqtt_broker_username'], CONFIG['mqtt_broker_password'], keepalive=60)
            client.set_callback(mqtt_callback)  #配置回调函数
            client.connect()
            client.subscribe(TOPIC)  #订阅主题
            client.publish(TOPIC, CONFIG['client_id'])
            print(f"MQTT Connected 、Subscribed and first publish message ->  {CONFIG['topic']}:{CONFIG['client_id']}")
            
        except Exception as e:
            print(e)
            
        while True:
            msg_count += 1 
            msg = f"Message {msg_count} from ESP32"
            if msg_count % 6  ==0 :
                try:
                    client.publish(CONFIG['topic'], msg)
                    print(f"send message to topic  {CONFIG['topic']}:{msg}")
                except Exception as e:
                    print(f"MQTT connection failed: {e}")

            #client.check_msg()
            #print(msg)
            time.sleep(3)  
                

                                    
                


