依赖包：
openpyxl
xlrd

python版本：3.6.4

使用文档：
### 一、读取文件
```python
# filename为文件路径，绝对路径和相对路径都可以
# encoding为可选参数，对应 xlrd的 encoding_overide，如果你不知道自己在干什么的话就不要设置
reader = ExcelReader(filename, [encoding])
```
#### 1、遍历行
行的格式有两种，一种返回数组形式，数组里的元素序号和表头对应， 如：
```python
# 文件如下
# col1， col2
# 1，2
# 3，4
for row in reader.rows():
	print(row)
# [1, 2]
# [3, 4]
```
另一种根据表头返回字典格式，如：
```python
# 文件如下
# col1， col2
# 1，2
# 3，4
for row in reader.dict_rows():
	print(row)
# {'col1': 1, 'col2': 2}
# {'col1': 3, 'col2': 4}
```
#### 2、获取表头
```python
reader.headers
#  ['col1', 'col2']
```
#### 3、获取行数和列数
```python
reader.col_num
reader.row_num
```
需要注意的是，这里的行数是包括表头在内的
#### 4、切换sheet
```python
reader.set_current_sheet(index=None, name=None)
```
index和 name只能选择一个，如果两个都使用了的话只优先使用 index。
特别注意，如果需要使用 name则需要使用关键字参数，如：
```python
reader.set_current_sheet(name='Sheet1')
```
### 二、写入文件
```python
# filename是保存文件的路径，如果文件已存在则覆盖
# headers是excel表的表头，必须在开始时设置
writer = ExcelWriter(filename, headers)
```
写入数据很简单，直接调用 write方法即可，如：
```python
writer.write(data)
```
data可以是列表或者字典或者元祖，如果是列表和元组的话则data的长度必须和表头相投
是字典的话则必须包含所有的表头，否则均无法写入数据。

特别注意：在未调用save函数时，所有数据均在内存中，只有调用 save函数之后数据才会保存到硬盘中去。

代码GitHub地址：https://github.com/geebos/cooltools/blob/master/excel_helper/excelhelper.py

