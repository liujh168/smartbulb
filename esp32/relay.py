'''
深圳市普中科技有限公司（PRECHIN 普中）
技术支持：www.prechin.net
PRECHIN
 普中
 
实验名称：继电器实验
接线说明：继电器模块-->ESP32 IO
         (REL)-->(25)
         
         继电器模块输出-->LED模块
         (COM)-->(3V3)
         (NO)-->(D1)
         
实验现象：程序下载成功后，继电器模块间隔一定时间吸合断开，吸合时D1指示灯亮，断开时灭
注意事项：

'''

#导入Pin模块
from machine import Pin
import time

#定义继电器控制对象
relay=Pin(25,Pin.OUT)   
    
#程序入口
if __name__=="__main__":
    i=0    
    while True:
        i=not i
        relay.value(i)
        time.sleep(1)
    


