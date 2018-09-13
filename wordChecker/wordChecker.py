#-*- coding: utf-8 -*
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import requests


class WordChecker(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.input_word = QLineEdit()
        self.display = QTextBrowser()
        self.cheack = QPushButton('查询')

        self.layout = QVBoxLayout()

        self.input_word.setPlaceholderText('输入要查询的字符串')
        self.input_word.selectAll()

        self.layout.addWidget(self.input_word)
        self.layout.addWidget(self.display)
        self.layout.addWidget(self.cheack)

        self.setWindowTitle('单词查询')
        self.setLayout(self.layout)

        self.setFocus()
        self.connect(self.cheack, SIGNAL('clicked()'), self.displayQueryResult)

    def displayQueryResult(self):
        word = self.getWord()
        query_result = self.useApiToQueryWord(word)
        result = self.dealWithTheQueryResult(query_result)

        self.display.clear()
        for t in result:
            self.display.append(t)

    def getWord(self):
        word = self.input_word.text()
        words = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if word[0] in words:
            word = {
                'word': word,
                'type': 'en'
            }
        else:
            word = {
                'word': word,
                'type': 'cn'
            }
        return word

    def useApiToQueryWord(self, word):
        api = 'http://dict-co.iciba.com/api/dictionary.php'
        params = {
            'w': word['word'],
            'key': '896E1A8D130A8021280960D903C7E8EA',
            'type': 'json',
        }
        r = requests.get(api, params=params)
        return {
            'query_result': r.json(),
            'type': word['type']
        }

    def dealWithTheQueryResult(self, query_result):
        if 'word_name' not in query_result['query_result']:
            return None

        if query_result['type'] == 'en':
            result = self.dealWithTheEnglishQueryResult(query_result['query_result'])
            return  result
        else:
            result = self.dealWithTheChineseQueryResult(query_result['query_result'])
            return result

    def dealWithTheEnglishQueryResult(self, query_result):
        try:
            word_name = query_result['word_name']
        except:
            return None

        result = word_name
        for t in query_result['symbols'][0]['parts']:
            item = '<p> <b> {} </b> {} </p>'.format(t['part'], '，'.join(t['means']))
            result = result + item
        return [result]

    def dealWithTheChineseQueryResult(self, query_result):
        means = query_result['symbols'][0]['parts'][0]['means']

        result = []
        for t in means:
            word = t['word_mean']
            word_result = self.useApiToQueryWord({'word': word, 'type': 'en'})
            deal_result = self.dealWithTheEnglishQueryResult(word_result['query_result'])
            if deal_result:
                result.append(deal_result[0])
        return result


app = QApplication(sys.argv)
dialog = WordChecker()
dialog.show()
app.exec_()

