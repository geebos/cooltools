# -*- coding: utf-8 -*
__author__ = 'geebos'
import os
from pypinyin import lazy_pinyin
'''

'''

class MarcItem:
    def __init__(self, encoding):
        self.encoding = encoding
        self.fileds = []
        self.header = []

    def addHeader(self, first, second):
        self.header.append(first)
        self.header.append(second)

    def addFiled(self, filed):
        tag = filed['tag']
        subfileds = filed['subfileds']

        tag, indicator = self._getTagAndIndicator(tag)

        if self._check_subfileds(subfileds):
            first, *rest = subfileds
            for t in first[1]:
                temp_subfileds = [(first[0], t)] + rest

                if tag in ['200', '701']:
                    temp_subfileds = self._addPinyinSubfiled(temp_subfileds)
                filedobj = self._getFiledObj(tag, indicator, temp_subfileds)
                self.fileds.append(filedobj)
        else:
            if tag in ['200', '701']:
                subfileds = self._addPinyinSubfiled(subfileds)

            filedobj = self._getFiledObj(tag, indicator, subfileds)
            self.fileds.append(filedobj)

    def _addPinyinSubfiled(self, subfileds):
        first, *rest = subfileds
        second = [('9', ' '.join(lazy_pinyin(first[1])).strip())]

        return [first]+second+rest

    #making name will kill me !!!
    def _check_subfileds(self, subfileds):
        sub = isinstance(subfileds[0][1], list)
        sub_1 = False
        for t in subfileds[1:]:
            sub_1 = isinstance(t[1], list)
            if sub_1:
                break
        if sub and not sub_1:
            return True
        elif not sub and not sub_1:
            return False
        elif not sub and sub_1:
            return False
        else:
            raise ValueError(f'Subfileds can not contains 2 list subfiled.\n{str(subfileds)}')


    def _getFiledObj(self, tag, indicator, subfileds):
        start = b'\x1F'
        end = b'\x1E'
        byte_subfileds = b''

        byte_subfileds = indicator.encode(self.encoding)+byte_subfileds

        for subfiled in subfileds:
            if len(subfiled) != 2:
                raise ValueError('Subfiled length should be 2.')

            if subfiled[0] == '':
                byte_subfiled = subfiled[1].encode(self.encoding)
            else:
                byte_subfiled = start+''.join(subfiled).encode(self.encoding)

            byte_subfileds = byte_subfileds+byte_subfiled
        byte_subfileds = byte_subfileds+end
        return (tag, len(byte_subfileds), byte_subfileds)

    def _getTagAndIndicator(self, tag):
        tag_len = len(tag)
        if tag_len == 3:
            if tag in ['001', '005']:
                return tag, ''
            else:
                return tag, '  '
        elif tag_len == 5:
            return tag[:3], tag[3:]
        else:
            raise ValueError('The tag should be xxx or xxxxx.')

    def getBinaryContent(self):
        ldr = self._getBinaryLDR()
        content = self._getBinaryContentFiled()
        subfiled = self._getCombinedSubfileds()
        return ldr+content+subfiled

    def _getBinaryLDR(self):
        item_length = self._fill_to_require_len(self._getItemLength(), '0', 5)
        data_start_location = self._fill_to_require_len(self._getDataStartLocation(), '0', 5)
        return (item_length+self.header[0]+data_start_location+self.header[1]).encode(self.encoding)

    def _getBinaryContentFiled(self):
        end = b'\x1E'
        start_location = 0
        byte_content_filed = b''

        for filed in self.fileds:
            tag = filed[0]
            length = self._fill_to_require_len(filed[1], '0', 4)
            location = self._fill_to_require_len(start_location, '0', 5)
            start_location+=filed[1]
            byte_content_filed=byte_content_filed+f'{tag}{length}{location}'.encode(self.encoding)
        byte_content_filed=byte_content_filed+end
        return byte_content_filed

    def _getCombinedSubfileds(self):
        end = b'\x1D'
        combined_subfileds = b''
        for filed in self.fileds:
            combined_subfileds=combined_subfileds+filed[2]
        combined_subfileds=combined_subfileds+end+b'\r\n'
        return combined_subfileds

    def _getItemLength(self):
        header = 24
        content = 12 * len(self.fileds) + 1
        combined_subfileds = 0 + 1
        for filed in self.fileds:
            combined_subfileds+=int(filed[1])
        return header+content+combined_subfileds

    def _getDataStartLocation(self):
        header = 24
        content = 12 * len(self.fileds) + 1
        return header+content

    def _fill_to_require_len(self, num, fill_char, require_length):
        if isinstance(num, str):
            str_num = num
        else:
            str_num = str(num)

        while len(str_num) < require_length:
            str_num=fill_char+str_num
        return str_num


class MarcWriter:
    def __init__(self, filepath):
        self.marcfile = self._get_file_obj(filepath)

    def __del__(self):
        self.marcfile.close()

    def writeOne(self, marcitem):
        self.marcfile.write(marcitem.getBinaryContent())
        self.marcfile.flush()

    def writeMany(self, marcitems):
        all = b''
        for item in marcitems:
            all=all+item.getBinaryContent()
        self.marcfile.write(all)
        self.marcfile.flush()

    def _get_file_obj(self, filepath):
        if self._file_exist(filepath):
            return open(filepath, 'ab')
        else:
            return open(filepath, 'wb')


    def _file_exist(self, filepath):
        if os.path.isfile(filepath):
            return True
        else:
            return False


if __name__ == '__main__':
    writer = MarcWriter('test_gbk.iso')
    m = MarcItem(encoding='gbk')
    m.addHeader('nam0 22', '   450 ')
    tags = [
        {'tag': '001', 'subfileds': [('', '2017012163')]},
        {'tag': '005', 'subfileds': [('', '20180725190411.0')]},
        {'tag': '010', 'subfileds': [('a', '978-7-117-22783-4'), ('d', 'CNY30.00')]},
        {'tag': '100', 'subfileds': [('a', '20180725d2016    em y0chiy0110    ea')]},
        {'tag': '1010 ', 'subfileds': [('a', 'chi')]},
        {'tag': '102', 'subfileds': [('a', 'CN'), ('b', '110000')]},
        {'tag': '105', 'subfileds': [('a', 'y   z   000yy')]},
        {'tag': '106', 'subfileds': [('a', 'r')]},
        {'tag': '2001 ','subfileds': [('a', '尘肺病的护理与康复'), ('f', '李智民 刘璐 张健杰')]},
        {'tag': '205', 'subfileds': [('a', '1版')]},
        {'tag': '210', 'subfileds': [('a', '北京'), ('c', '人民卫生出版社'), ('d', '2016.')]},
        {'tag': '215', 'subfileds': [('a', '27页'), ('d', '24cm')]},
        {'tag': '330', 'subfileds': [('a', '该书主要介绍尘肺病的基础知识、诊断依据、治疗原则、综合评估、饮食治疗、运动治疗、康复训练、药物疗法、症状护理、急慢性并发症的防治、生活调护、重要记录等。该书以紧跟职业病防治以及康复新形势、普及新知识、适应社会需要为特色，语言通俗，图文并茂，适合从事医疗卫生和职业安全健康人员、相关行业管理人员、尘肺病患者阅读。')]},
        {'tag': '6060 ', 'subfileds': [('axyz', '尘肺－护理；尘肺－康复')]},
        {'tag': '690', 'subfileds': [('a', 'R473.59；R598.209'), ('v', '5')]},
        {'tag': '701 0','subfileds': [('a', ['李智民', ' 刘璐', ' 张健杰']), ('4', ' 主编')]},

    ]

    for t in tags:
        m.addFiled(t)

    writer.writeMany([m, m, m, m, m])
    writer.writeOne(m)