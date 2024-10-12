一、项目简介
```text
代号：摸鱼
宗旨：通过小工具提高工作效率。
```
二、里程碑

v0.0.1
- 可以把多个数据源组织成二维表，然后转换为json格式
- 把多个数据源合并，可以定义表达式，合并的时候新增key
- 把合并好的数据写入到excel
- 合并时的表达式目前只支持 +-*/% 运算符，并且只支持整数和小数

v0.0.2
- 删除没必要的文件

v0.0.3
```text
0.0.3x的所有更新记录
```
- 把包名从module换为SlackOffMj
- 修复模块找不到的问题
- 优化generator，可选填filter，folders可填文件和路径

v0.0.4
- 把包名从SlackOffMj改成slackoff，新增toj模块，模块功能就是0.0.1的全部功能
- 新增generator默认配置，XlsxReconciliation默认实现init_iterator，iterator_item的功能
- 在XlsxReconciliation中新增默认配置sheet，里边包含sheet的名字（name）和起始行（min_row）

v0.0.5
- 给generator的rule属性新增表达式处理，使用时rule必须为字符串或者返回字符串并且前缀为exper:
- 单独把表达式解析抽出，并使用python内置的abs语法抽象树做表达式运算处理

v0.1.0
- generator的rule规则可以配置为数组，只要配置中不存在rule，只存在children，会默认生成为数组
- generator新增toString方法，存在rule的情况下，可以把数组转换为目标字符串

v0.1.1
- 去除表达式exper:前缀
- 修复generator的rule没有上下文的问题

v0.1.2
- 写入excel时，row支持数组和字典访问、支持正则表达式，col支持表达式
- 修复generator的rule作为表达式时可能报错的bug，取消函数和类函数返回字符串作为表达式去运算的功能
- 给toXlsx的writer.col加入表达式功能
- 优化merge表达式实现

问题
- generator的children的rule找不到值时，应该给上None。如果不给上None，children对应的数组数量对应不上children的数量。

v0.1.3
- 给toXlsx.writer新增过滤功能，只需定义filter，如果不定义filter，默认不对任何数据进行过滤

v0.1.4
- 修复合并时，过滤失败的问题
- 修复generator的children解析为数组时，值的位置和children对应位置不一致的问题

v0.1.5
- 新增合并表格功能

三、slackoff.toj参数说明
- generator[].rule
```text
生成key，可以是函数，也可以是类。如果是类的话，必须有rule函数。
函数传入一个参数，是一个字典，具体如下：
{
    "filename": 文件名称
    "row": 一行源数据
    "this": 同级别已经解析好的json
}
```
