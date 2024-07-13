'''
接线说明：DS18B20温度传感器模块-->ESP32 IO
         (DS)-->(13)
'''

#导入Pin模块
from machine import Pin
import time
import onewire
import ds18x20

GPIO_T = 13 

#定义DS18B20控制对象
ds18b20=ds18x20.DS18X20(onewire.OneWire(Pin(GPIO_T)))


#程序入口
if __name__=="__main__":
    roms = ds18b20.scan()  #扫描是否存在DS18B20设备
    print("DS18B20初始化成功！")
    while True:
        ds18b20.convert_temp()
        time.sleep(1)
        for rom in roms:
            print("DS18B20检测温度：%.2f°C" %ds18b20.read_temp(rom))
        
