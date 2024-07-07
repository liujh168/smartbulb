'''
Dht 类接受一个引脚参数用于连接 DHT11 传感器。类中有一个 measure_data 方法用于执行测量和数据处理。
'''
from machine import Pin
import time
import dht

class Dht:
    def __init__(self, pin):
        self.dht = dht.DHT11(Pin(pin))

    def measure_data(self):
        time.sleep(1)  # 首次启动间隔 1 秒让传感器稳定
        while True:
            self.dht.measure()  # 调用 DHT 类库中测量数据的函数
            temp = self.dht.temperature()
            humi = self.dht.humidity()
            if temp is None:
                print("DHT11 传感器检测失败！")
            else:
                print("temp=%d°C  humi=%dRH" % (temp, humi))
            time.sleep(2)  # 如果延时时间过短，DHT11 温湿度传感器不工作
    
#程序入口
if __name__=="__main__":
    dht_obj = Dht(27)  # 创建 Dht 对象并指定引脚
    dht_obj.measure_data()  # 调用测量数据方法