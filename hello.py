from flask import Flask, jsonify, request, render_template,  make_response
import subprocess
import paho.mqtt.client as mqtt

app = Flask(__name__)

# 设备状态
status_info = {
    "deviceName": "light_ljh",
    "productKey": "product_key",
    "status": {
        "color": "red",
        "brightness": 70,
        "powerStatus": "on"
        # 其他状态信息...
    }
}

#app.config['JSON_AS_ASCII'] = False  # 允许jsonify返回非ASCII字符

# MQTT配置
MQTT_BROKER = '120.26.241.36'
MQTT_PORT = 1083
MQTT_TOPIC = 'mytest'
MQTT_USERNAME='ljh'
MQTT_PASSWORD='56865686'

def interact_with_console_app():
    # 构建命令行参数列表，这里假设控制台程序名为 'your_console_app'
    command = ['pikafish']

    # 使用Popen启动控制台程序，同时将stdin, stdout, stderr设置为PIPE
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        print("uci 来了。。。。。。。。")
        # 这里可以发送一些初始输入给控制台程序
        initial_input = "uci\nisready\n"
        process.stdin.write(initial_input)
        process.stdin.flush()  # 确保输入被发送

        # 读取控制台程序的输出
        output = process.stdout.read()  # 读取输出，这里使用阻塞读取
        print("程序输出：")
        print(output)

        # 可以继续发送输入，例如：
        more_input = "go depth 16\nstop\nbye\n"
        process.stdin.write(more_input)
        process.stdin.flush()

        # 再次读取输出
        more_output = process.stdout.read()
        print("更多输出：")
        print(more_output)

    finally:
        # 完成交互后，关闭stdin，以通知控制台程序输入结束
        print("uci uci pikafish 退出函数")
        process.stdin.close()
        # 等待控制台程序结束
        process.wait()

# MQTT回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"收到信息了 Received:  `{msg.payload.decode('utf-8')}`  from topic: `{msg.topic}`")
    message_str = msg.payload.decode('utf-8')    #解码后，字节序列 变为 字符串 才可以比较

    if message_str == "poweron":
        status_info["status"]["powerStatus"] = "on"
        print("灯是打开状态的！")
    if message_str == "poweroff":
        status_info["status"]["powerStatus"] = "off"
        print("灯是关闭状态的！")

# MQTT客户端
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect_timeout = 30  # 例如，设置为30秒
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# 定义UI路由
@app.route('/ui/<name>')
def ui_name(name):
    if name == "light":
        powerStatus = status_info["status"]["powerStatus"]
        print(f"powerStatus:{powerStatus}")
        return render_template('light.html', powerStatus=powerStatus)
    elif name == "mqtt":
        return render_template('mqtt.html')
    elif name == "TV":
        return render_template('TV.html')
    else:
        return render_template('default.html')

# RESTful API
@app.route('/api/on', methods=['GET'])
def light_power_on():
    message = request.args.get('msg', 'on')
    print("publish message to MQTT: " + message)
    mqtt_client.publish(MQTT_TOPIC, message)
    return jsonify({'status': 'success', 'message': 'light_power_on sent to MQTT', 'newImgSrc':'/static/on.png'})

@app.route('/api/off', methods=['GET'])
def light_power_off():
    message = request.args.get('msg', 'off')
    print("publish message to MQTT: " + message)
    mqtt_client.publish(MQTT_TOPIC, message)
    return jsonify({'status': 'success', 'message': 'light_power_off sent to MQTT', 'newImgSrc':'/static/off.png'})

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message')
    mqtt_client.publish(MQTT_TOPIC, message)
    return jsonify({'status': 'success', 'message': 'Message sent to MQTT'})

@app.route('/api/pub', methods=['GET'])
def publish_message():
    message = request.args.get('msg', '这是个缺省消息')
    print("publish message to MQTT: " + message)
    mqtt_client.publish(MQTT_TOPIC, message)

    # 使用make_response来创建响应对象
    #response = make_response(jsonify({'status': 'success', 'message': message.encode('utf-8')}))
    # 手动设置Content-Type和charset=utf-8
    #response.headers['Content-Type'] = 'application/json; charset=utf-8'
    
    return jsonify({'status': 'success', 'message sent to MQTT:': message})
    #return response

@app.route('/api/status', methods=['GET'])
def status():
    # MQTT 或 灯的状态或其他信息
    powerstatus = status_info["status"]["powerStatus"]
    brightness = status_info["status"]["brightness"]
    color = status_info["status"]["color"]

    #print("SmartBulb PowerStatus: " + powerstatus )

    json_status = jsonify({
        'status':'MQTT is running', 
        'powerstatus':powerstatus, 
        'brightness':brightness, 
        'color':color
    })
    print(json_status)

    mqtt_client.publish(MQTT_TOPIC, "status")  #返回之前查询一下，更新状态信息

    return json_status


print("\n" + __name__+"\n")
print("usage：  http://120.26.241.36/api/pub?msg=on[off]     开【关】灯\n")
print("usage：  http://120.26.241.36/api/status  获取状态\n")

if __name__ == '__main__':
    
    #interact_with_console_app()
    app.run(debug=False, host='0.0.0.0', port=5000)






