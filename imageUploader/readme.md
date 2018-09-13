关键代码：
-----

cookie：简书登录之后的 cookie
filepath：要上传图片的绝对路径，同目录下可直接使用名字
filename：要上传图片的名字（随意取）

```python
def uploadImage(cookie, filepath, filename):
    upload_url = 'https://upload.qiniup.com/'
    token_url = 'https://www.jianshu.com/upload_images/token.json?filename={}'.format(filename)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Cookie': cookie,
    }

    response = requests.get(token_url, headers=headers)
    response.encoding = response.apparent_encoding
    token_and_key = json.loads(response.text)

    with open(filepath, 'rb') as file:
        files = {
            'file': (filename, file),
            'token': (None, token_and_key['token']),
            'key': (None, token_and_key['key']),
        }
        response = requests.post(upload_url, headers=headers, files=files)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)['url']
```

PyQt4封装后的代码：
-------------

与脚本同目录下创建一个名为 config的文件（没有后缀名），用文本编辑器打开（别用记事本，如果用记事本打开并保存过请删除重建），将简书登录后的 cookie直接粘贴进去（不需要多余的字符，只要 cookie就行）
代码附上：

```python
#-*- coding: utf-8 -*
__author__ = 'geebos'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import requests
import json
import sys


class UploadBox(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        self.data = {}
        self.cookie  = self.getCookie().strip()

        self.location_lable = QLabel("图片位置:")
        self.url_lable = QLabel("图片链接:")
        self.show_path = QLineEdit()
        self.show_result = QTextBrowser()
        self.select_button = QPushButton("选择图片")
        self.comfir_button = QPushButton("确认上传")

        layout.addWidget(self.location_lable)
        layout.addWidget(self.show_path)
        layout.addWidget(self.url_lable)
        layout.addWidget(self.show_result)
        layout.addWidget(self.select_button)
        layout.addWidget(self.comfir_button)

        self.setWindowTitle("图片上传")
        self.setLayout(layout)

        self.select_button.clicked.connect(self.selectFile)
        self.comfir_button.clicked.connect(self.uploadImage)

    def getCookie(self):
        try:
            with open('config', 'r') as f:
                return f.readline()
        except Exception:
            QMessageBox.warning(self, "提示", "配置文件 config出错")

    def selectFile(self):
        filepath = QFileDialog.getOpenFileName(self, caption="选择图片", directory='.', filter="ALL FILES (*.*)")
        self.show_path.setText(filepath)
        self.data['filepath'] = filepath

    def uploadImage(self):
        if 'filepath' in self.data:
            filepath = self.data['filepath']
            filename = filepath.split('/')[-1]
            print(filename)
        else:
            return

        upload_url = 'https://upload.qiniup.com/'
        token_url = 'https://www.jianshu.com/upload_images/token.json?filename={}'.format(filename)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
            'Cookie': self.cookie,
        }

        response = requests.get(token_url, headers=headers)
        response.encoding = response.apparent_encoding
        token_and_key = json.loads(response.text)

        if 'token' not in token_and_key:
            self.show_result.clear()
            QMessageBox.warning(self, "提示", "格式错误，请选择图片")
            return

        with open(filepath, 'rb') as file:
            files = {
                'file': (filename, file), 'token': (None, token_and_key['token']), 'key': (None, token_and_key['key']),
            }
            response = requests.post(upload_url, headers=headers, files=files)
            response.encoding = response.apparent_encoding
            result = json.loads(response.text)

            if 'url' in result:
                self.show_result.clear()
                self.show_result.append(result['url'])
            else:
                self.show_result.clear()
                QMessageBox.Information(self, "提示", "上传失败，请检查 cookie是否有效")


app = QApplication(sys.argv)
dialog = UploadBox()
dialog.show()
app.exec_()
```

pyinstaller生成的可执行文件：
--------------------

使用方法同脚本：
https://pan.baidu.com/s/1qFdVcttwZdRS97jFgXpKTA
更多干货请关注简书账号：[python爬虫猫](https://www.jianshu.com/u/472a595d244c)