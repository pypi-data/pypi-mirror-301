# Mysql random data generation

This is an auxiliary package for learning Mysql, 
and the I feel that inserting some test data is too 
cumbersome to enter manually, 
so I write a method that generates this 
data **randomly** and can **automatically** write it 
in Mysql language and save it to a text file.
Currently, only insert into generation is supported.


Only Chinese is supported.

0.1.6 更多信息通过get_help()与get_demo()查看

pandas的帮助信息：
```python
import mysql_study_datamaker_CN.pd_datamaker as pdk
print(pdk.get_demo()) # 查看如何使用 pandas随机生成的案例
```
mysql的帮助信息
```python
import mysql_study_datamaker_CN.datamaker as dm
print(dm.get_demo()) # 获取 mysql 相关的案例
print(dm.get_help()) # 获取 mysql 相关的帮助
```
使用案例(mysql) 1：
实例1，生成单一数据
姓名，性别，年龄，城市
```python
import mysql_study_datamaker_CN.datamaker as dm
one = dm.DataMaker(20, ("姓名", "性别", "年龄", "城市"))
one.get_data()
```

使用案例(mysql) 2：
示例2，员工信息
姓名，性别，生日，年龄，身份证，部门，手机，100人
```python
import mysql_study_datamaker_CN.datamaker as dm
one = dm.DataMaker(50, ("姓名", "性别", "工号", "分数语文", "分数数学", "分数英语"),
                work_head="2024.三班", work_numwidth=2)
one.get_data("insert_into")
```

使用案例(mysql) 3：
示例3，员工信息
姓名，性别，生日，年龄，身份证，部门，手机，100人
```python
import mysql_study_datamaker_CN.datamaker as dm
one = dm.DataMaker(100, ("姓名", "性别", "生日", "年龄", "身份证", "部门", "手机"))
one.get_data("insert_into")
```

使用案例(pandas.DataFrame) 4：
示例4，DataFrame对象，该对象的随机成绩
列名：科目
行名：姓名
```python
import mysql_study_datamaker_CN.pd_datamaker as pdk
names = ["Tom",
         "Bob",
         "Jerry",
         "Lucy",
         "Lily",
         "Mike",
         "Tony",
         "Amber",
         "Kevin",
         "Peter"]
d1 = pdk.to_DataFrame_maker(n=9, low=80, high=150, people=10, names=names)
print(d1)
```