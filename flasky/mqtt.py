from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import subprocess
from flask import  make_response

app = Flask(__name__)

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
        print("pikafish 来了。。。。。。。。")
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
    #message_str = msg.payload.decode('utf-8')
    print(f"收到信息了 Received:  `{msg.payload.decode('utf-8')}`  from topic: `{msg.topic}`")

# MQTT客户端
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect_timeout = 30  # 例如，设置为30秒
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# RESTful API
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
    # 这里可以添加一些逻辑来获取MQTT的状态或其他信息
    return jsonify({'status': 'MQTT is running'})


print("\n" + __name__+"\n")
print("usage：  http://120.26.241.36/api/pub?msg=on[off]     开【关】灯\n")
print("usage：  http://120.26.241.36/api/status  获取状态\n")

if __name__ == '__main__':
    
    #interact_with_console_app()
    app.run(debug=False, host='0.0.0.0', port=5000)






