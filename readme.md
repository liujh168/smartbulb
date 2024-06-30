<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MQTT客户端界面</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 90%;
            max-width: 600px;
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"],
        input[type="number"] {
            width: calc(100% - 22px);
            padding: 8px;
            margin-bottom: 5px;
        }
        button {
            padding: 10px 20px;
            cursor: pointer;
            margin-right: 5px;
        }
        #messages {
            margin-top: 20px;
            width: 100%;
            height: 200px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            box-sizing: border-box;
            background-color: #f9f9f9;
        }
        #statusMessage {
            margin-bottom: 10px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.1.0/paho-mqtt.min.js"></script> 
</head>
<body>
    <div class="container">
        <h1>MQTT客户端界面</h1>
        <div class="form-group">
            <label for="broker">代理服务器地址：</label>
            <input type="text" id="broker" placeholder="输入代理服务器地址" value="broker.hivemq.com">
        </div>
        <div class="form-group">
            <label for="port">端口：</label>
            <input type="number" id="port" value="8000">
        </div>
        <div class="form-group">
            <label for="clientID">客户端ID：</label>
            <input type="text" id="clientID" placeholder="输入客户端ID">
        </div>
        <div class="form-group">
            <label for="topic">主题：</label>
            <input type="text" id="topic" placeholder="输入主题">
        </div>
        <div class="form-group">
            <label for="message">消息内容：</label>
            <input type="text" id="message" placeholder="输入消息内容">
        </div>
        <button id="connect">连接</button>
        <button id="disconnect">断开连接</button>
        <button id="subscribe">订阅主题</button>
        <button id="publish">发布消息</button>
        <div id="statusMessage" style="color: grey;"></div> <!-- 提示信息显示区域 -->
        <div id="messages"></div>
    </div>

    <script>
        var client; // MQTT客户端实例
        var statusMessageDiv = document.getElementById('statusMessage'); // 用于显示状态信息的元素

        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById('connect').addEventListener('click', connect);
            document.getElementById('disconnect').addEventListener('click', disconnect);
            document.getElementById('subscribe').addEventListener('click', subscribe);
            document.getElementById('publish').addEventListener('click', publish);
        });

        function connect() {
            var broker = document.getElementById('broker').value;
            var port = parseInt(document.getElementById('port').value, 10) || 1883;
            var clientID = document.getElementById('clientID').value;

            // 清除之前的状态信息
            statusMessageDiv.textContent = "正在连接...";
            statusMessageDiv.style.color = "grey";

            // 创建MQTT客户端实例
            client = new Paho.MQTT.Client(broker, port, clientID);

            // 设置连接选项
            var options = {
                timeout: 3,
                useSSL: false,
                onSuccess: onConnect,
                onFailure: function (message) {
                    onFailureConnect(message);
                }
            };

            // 设置消息处理函数
            client.onMessageArrived = onMessageArrived;

            // 连接到MQTT代理
            client.connect(options);
        }

        function onConnect() {
            console.log("Connected to MQTT broker.");
            statusMessageDiv.textContent = "连接成功";
            statusMessageDiv.style.color = "green";
            // 订阅主题的示例代码
            var topic = document.getElementById('topic').value;
            client.subscribe(topic);
        }

        function onFailureConnect(message) {
            console.log("Connection failed: " + message.errorMessage);
            statusMessageDiv.textContent = "连接失败: " + message.errorMessage;
            statusMessageDiv.style.color = "red";
        }

        function disconnect() {
            if (client) {
                client.disconnect();
                console.log("Disconnected from MQTT broker.");
                statusMessageDiv.textContent = "已断开连接";
                statusMessageDiv.style.color = "grey";
            }
        }

        function subscribe() {
            var topic = document.getElementById('topic').value;
            if (client && client.isConnected()) {
                client.subscribe(topic);
                console.log("Subscribed to topic: " + topic);
            }
        }

        function publish() {
            var topic = document.getElementById('topic').value;
            var message = document.getElementById('message').value;
            if (client && client.isConnected()) {
                var payload = new Paho.MQTT.Message(message);
                payload.destinationName = topic;
                client.send(payload);
                console.log("Published message to topic: " + topic);
            }
        }

        function onMessageArrived(message) {
            console.log("Received message: " + message.payloadString + " from topic: " + message.destinationName);
            // 将接收到的消息显示在界面上
            var messagesDiv = document.getElementById('messages');
            var p = document.createElement('p');
            p.textContent = "收到消息: " + message.payloadString + " 来自主题: " + message.destinationName;
            messagesDiv.appendChild(p);
            messagesDiv.scrollTop = messagesDiv.scrollHeight; // 自动滚动到底部
        }
    </script>
</body>
</html>
