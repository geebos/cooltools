# -*- coding: utf-8 -*
__author__ = 'geebos'
import os


class MarcItem:
    def __init__(self):
        self._fields = []
        self._header = None

    def set_header(self, first, second):
        self._header = (first, second)

    def get_header(self):
        if hasattr(self, '_header'):
            return self._header
        else:
            return ('nam0 22', '   450 ')

    def get_fields(self):
        return self._fields

    def add_field(self, field):
        self._check_field(field)
        self._fields.append(field)

    def _check_field(self, field):
        if not ('tag' in field and 'indicator' in field and 'subfields' in field):
            raise ValueError('a field must has tag, indicator and subfields.')
        if len(field['subfields']) == 0:
            raise ValueError('subfields can not be an empty list.')
        if len(field['tag']) != 3:
            raise ValueError("tag's length should be 3.")
        if len(field['indicator']) != 2:
            raise ValueError("indicator's length should be 2.")

    def __str__(self):
        result = ''
        for t in self._fields:
            result += str(t) + '\n'
        return result


class MarcWriter:
    def __init__(self, filepath, encoding='gbk'):
        self.marcfile = self._get_file_obj(filepath)
        self.encoding = encoding

    def __del__(self):
        self.marcfile.close()

    def writeOne(self, marcitem):
        self.marcfile.write(self._transform_to_bytes(marcitem))
        self.marcfile.flush()

    def writeMany(self, marcitems):
        all = b''
        for item in marcitems:
            all=all+self._transform_to_bytes(item)
        self.marcfile.write(all)
        self.marcfile.flush()

    def _get_file_obj(self, filepath):
        if os.path.isfile(filepath):
            return open(filepath, 'ab')
        else:
            return open(filepath, 'wb')

    def _transform_to_bytes(self, item):
        fields = item.get_fields()

        content = b''
        data_area = b''
        length = 0
        for field in fields:
            if field['tag'] in ['001', '005']:
                data = field['subfields'][0][1].encode(self.encoding) + b'\x1e'
            else:
                data = self._get_binary_data(field['indicator'], field['subfields'])

            data_area += data
            content += ''.join((field['tag'], self._fill_to(len(data), '0', 4), self._fill_to(length, '0', 5)))\
                        .encode(self.encoding)
            length += len(data)
        data_area += b'\x1e'
        content += b'\x1e'

        data_base = 24 + len(content)
        item_length = 24 + len(content) + len(data_area) + 1
        first, second = item.get_header()
        header = ''.join(
                        (self._fill_to(item_length, '0', 5),
                         self._fill_to(first, ' ', 7),
                         self._fill_to(data_base, '0', 5),
                         self._fill_to(second, ' ', 7))
                    ).encode(self.encoding)

        return header + content + data_area + b'\x1d' + b'\r\n'

    def _get_binary_data(self, indicator, subfields):
        subfields_end = b'\x1e'
        split = b'\x1f'

        data = b'' + indicator.encode(self.encoding)
        for t in subfields:
            print(t)
            data += (split+''.join(t).encode(self.encoding))
        data += subfields_end

        return data

    def _fill_to(self, num, fill_char, require_length):
        if isinstance(num, str):
            str_num = num
        else:
            str_num = str(num)

        while len(str_num) < require_length:
            str_num=fill_char+str_num
        return str_num

class MarcReader:
    def __init__(self, filepath, encoding='gbk', ignor_error=False):
        self.file = self._get_file_obj(filepath)
        self.encoding = encoding
        self.ignor_error = ignor_error

    def __del__(self):
        self.file.close()

    def _get_file_obj(self, filepath):
        if os.path.isfile(filepath):
            return open(filepath, 'rb')
        else:
            raise ValueError(f'file {filepath} do not exist!')

    def items(self):
        for row in self.file:
            row = self.clear_row(row)

            header = row[:24]

            try:
                if len(row) != int(header[:5]):
                    raise Exception()
                row = row.replace(b'\x1d', b'')

                data_base = int(header[12:17])
                contents = (row[24:data_base].decode()[(i * 12):((i+1) * 12)] for i in
                            range(int((data_base-24) / 12)))
                data = row[data_base:]

                marcitem = MarcItem()
                for item in contents:
                    tag = str(item[:3])
                    length = int(item[3:7])
                    location = int(item[7:])

                    item_data = data[location:(location+length)]\
                                .replace(b'\x1e', b'').split(b'\x1f')

                    if tag.startswith('00'):
                        marcitem.add_field({
                            'tag': tag,
                            'indicator':'  ',
                            'subfields':[('', item_data[0].decode(self.encoding))]
                        })
                    else:
                        indicator = item_data[0].decode(self.encoding)
                        subfields = []

                        for i in range(1,len(item_data)):
                            temp_data = item_data[i].decode(self.encoding)
                            subfields.append((temp_data[0], temp_data[1:]))

                        marcitem.add_field({
                            'tag': tag,
                            'indicator': indicator,
                            'subfields': subfields
                        })
                yield marcitem
            except:
                if not self.ignor_error:
                    raise ValueError('error row in marcfile.')

    def clear_row(self, row):
        if row.endswith(b'\n'):
            row = row[:-1]
        if row.endswith(b'\r'):
            row = row[:-1]
        if row.endswith(b'\n\r'):
            row = row[:-2]
        return row



if __name__ == '__main__':
    # writer = MarcWriter('test_gbk.iso')
    # m = MarcItem()
    # m.set_header('nam0 22', '   450 ')
    # tags = [
    #     {'tag': '001', 'indicator':'  ', 'subfields': [('', '2017012163')]},
    #     {'tag': '005', 'indicator':'  ', 'subfields': [('', '20180725190411.0')]},
    #     {'tag': '010', 'indicator':'  ', 'subfields': [('a', '978-7-117-22783-4'), ('d', 'CNY30.00')]},
    #     {'tag': '100', 'indicator':'  ', 'subfields': [('a', '20180725d2016    em y0chiy0110    ea')]},
    #     {'tag': '101', 'indicator':'0 ', 'subfields': [('a', 'chi')]},
    #     {'tag': '102', 'indicator':'  ', 'subfields': [('a', 'CN'), ('b', '110000')]},
    #     {'tag': '105', 'indicator':'  ', 'subfields': [('a', 'y   z   000yy')]},
    #     {'tag': '106', 'indicator':'  ', 'subfields': [('a', 'r')]},
    #     {'tag': '200', 'indicator':'1 ', 'subfields': [('a', '尘肺病的护理与康复'), ('f', '李智民 刘璐 张健杰')]},
    #     {'tag': '205', 'indicator':'  ', 'subfields': [('a', '1版')]},
    #     {'tag': '210', 'indicator':'  ', 'subfields': [('a', '北京'), ('c', '人民卫生出版社'), ('d', '2016.')]},
    #     {'tag': '215', 'indicator':'  ', 'subfields': [('a', '27页'), ('d', '24cm')]},
    #     {'tag': '330', 'indicator':'  ', 'subfields': [('a', '该书主要介绍尘肺病的基础知识、诊断依据、治疗原则、综合评估、饮食治疗、运动治疗、康复训练、药物疗法、症状护理、急慢性并发症的防治、生活调护、重要记录等。该书以紧跟职业病防治以及康复新形势、普及新知识、适应社会需要为特色，语言通俗，图文并茂，适合从事医疗卫生和职业安全健康人员、相关行业管理人员、尘肺病患者阅读。')]},
    #     {'tag': '606', 'indicator':'0 ', 'subfields': [('axyz', '尘肺－护理；尘肺－康复')]},
    #     {'tag': '690', 'indicator':'  ', 'subfields': [('a', 'R473.59；R598.209'), ('v', '5')]},
    #     {'tag': '701', 'indicator':' 0', 'subfields': [('a', '李智民 刘璐 张健杰'), ('4', ' 主编')]},
    #
    # ]
    #
    # for t in tags:
    #     m.add_field(t)
    #
    # writer.writeOne(m)
    reader = MarcReader('test_gbk.iso')
    print(reader.items().__next__())