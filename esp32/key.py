'''
深圳市普中科技有限公司（PRECHIN 普中）
技术支持：www.prechin.net
PRECHIN
 普中
 
实验名称：按键控制实验
接线说明：按键模块-->ESP32 IO
         (K1-K4)-->(14,27,26,25)
         
         LED模块-->ESP32 IO
         (D1-D4)-->(15,2,0,4)
         
实验现象：程序下载成功后，操作K1键控制D1指示灯亮灭；操作K2键控制D2指示灯亮灭；
         操作K3键控制D3指示灯亮灭；操作K4键控制D4指示灯亮灭；
注意事项：

'''

#导入Pin模块
from machine import Pin
import time

#定义按键控制对象
key1=Pin(14,Pin.IN,Pin.PULL_UP)
key2=Pin(27,Pin.IN,Pin.PULL_UP)
key3=Pin(26,Pin.IN,Pin.PULL_UP)
key4=Pin(25,Pin.IN,Pin.PULL_UP)

#定义LED控制对象
led1=Pin(15,Pin.OUT)
led2=Pin(2,Pin.OUT)
led3=Pin(0,Pin.OUT)
led4=Pin(4,Pin.OUT) 

#定义按键键值
KEY1_PRESS,KEY2_PRESS,KEY3_PRESS,KEY4_PRESS=1,2,3,4
key_en=1
#按键扫描函数
def key_scan():
    global key_en  #全局变量
    if key_en==1 and (key1.value()==0 or key2.value()==0 or
                      key3.value()==0 or key4.value()==0 ):
        time.sleep_ms(10)  #消斗
        key_en=0
        if key1.value()==0:
            return KEY1_PRESS
        elif key2.value()==0:
            return KEY2_PRESS
        elif key3.value()==0:
            return KEY3_PRESS
        elif key4.value()==0:
            return KEY4_PRESS
    elif key1.value()==1 and key2.value()==1 and key3.value()==1 and key4.value()==1:
        key_en=1
    return 0

#程序入口
if __name__=="__main__":
    key=0
    i_led1,i_led2,i_led3,i_led4=0,0,0,0  #定义变量，用于LED状态翻转
    led1.value(i_led1)  #初始化LED，熄灭状态
    led2.value(i_led2)
    led3.value(i_led3)
    led4.value(i_led4)
    while True:
        key=key_scan()  #按键扫描
        if key==KEY1_PRESS:  #K1键按下
            i_led1=not i_led1
            led1.value(i_led1)
        elif key==KEY2_PRESS:  #K2键按下
            i_led2=not i_led2
            led2.value(i_led2)
        elif key==KEY3_PRESS:  #K3键按下
            i_led3=not i_led3
            led3.value(i_led3)
        elif key==KEY4_PRESS:  #K4键按下
            i_led4=not i_led4
            led4.value(i_led4)

