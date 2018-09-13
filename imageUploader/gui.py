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