"""

在EC2实例上安装PyCharm的步骤如下：

登录到EC2实例：使用SSH连接到您的EC2实例。例如，在终端中输入以下命令：

$ ssh -i /path/to/key.pem ec2-user@<ec2-public-ip-address>
其中，/path/to/key.pem 是您EC2密钥对文件的路径，<ec2-public-ip-address> 是您EC2实例的公共IP地址。

下载PyCharm：在终端中输入以下命令下载PyCharm Community Edition（免费版）：

$ wget https://download-cf.jetbrains.com/python/pycharm-community-2021.2.2.tar.gz
如果您想下载PyCharm Professional Edition（付费版），请访问JetBrains官网并按照提示下载最新版本。

解压缩PyCharm：在终端中输入以下命令解压缩PyCharm安装包：

$ tar -xzvf pycharm-community-2021.2.2.tar.gz
启动PyCharm：在终端中输入以下命令启动PyCharm：

$ cd pycharm-community-2021.2.2/bin/
$ sh pycharm.sh
按照提示进行安装：在第一次运行PyCharm时，将提示您进行一些初始设置和配置。根据您的需求和偏好进行选择，并完成安装向导。

完成安装后，您可以在PyCharm中开始编写Python代码。请注意，这仅是基本安装过程，您可能需要根据自己的需求和环境进行更改和配置。







"""









# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# 从配置文件中settings加载配置
app.config.from_pyfile('settings.py')
@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        messages = request.form.get("prompt", None)
        apiKey = request.form.get("apiKey", None)

        if messages is None:
            return jsonify({"error": {"message": "请输入prompt!", "type": "invalid_request_error"}})

        if apiKey is None:
            apiKey = app.config['OPENAI_API_KEY']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apiKey}",
        }
        # json串转对象
        prompt = json.loads(messages)

        data = {
            "messages": prompt,
            "model": "gpt-3.5-turbo",
            "max_tokens": 2048,
            "temperature": 0.5,
            "top_p": 1,
            "n": 1,
        }
        resp = requests.post(url=app.config["URL"], headers=headers, json=data).json()
        return jsonify(resp["choices"][0]["message"])
    except KeyError:
        return jsonify(resp)

if __name__ == '__main__':
    # app.run(port=5002)
    # app.run(host="192.168.0.101", port=8000)
    app.run(host='0.0.0.0')
