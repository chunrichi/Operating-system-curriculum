- [进程调度模拟程序](#进程调度模拟程序)
- [目录结构](#目录结构)
- [如何使用](#如何使用)
- [相关知识-tkinter](#相关知识-tkinter)
        - [控件及属性](#控件及属性)
                - [1. Button](#1-button)
                - [2. Label](#2-label)
                - [3.Frame](#3frame)
                - [4. Entry](#4-entry)
        - [几何管理方法](#几何管理方法)
        - [Variable类](#variable类)

## 进程调度模拟程序

时间片轮转调度算法原理的基础上的一个可视化的算法模拟程序。

## 目录结构
```
code
│  main.py
│  prc.py
│  README.md
│  save_log.py
│
├─log
│      2018-06-22-log.txt
│
├─sourse
│      Prc.txt
│
└─__pycache__
        prc.cpython-36.pyc
        save_log.cpython-36.pyc
```

## 如何使用

在当前目录终端下直接用python运行 `main.py`

## 相关知识-tkinter

不全

### 控件及属性

#### 1. Button
控件属性

| 参数             | 描述                                                  |
| ---------------- | ----------------------------------------------------- |
| height           | 组件的高度（所占行数）                                |
| width            | 组件的宽度（所占字符个数）                            |
| fg               | 前景字体颜色                                          |
| bg               | 背景颜色                                              |
| activebackground | 按钮按下时的背景颜色                                  |
| activeforeground | 按钮按下时的前景颜色                                  |
| justify          | 多行文本的对齐方式，可选参数为： LEFT、 CENTER、RIGHT |
| padx             | 文本左右两侧的空格数（默认为1）                       |
| pady             | 文本上下两侧的空格数（默认为1）                       |


#### 2. Label
控件属性

| 参数         | 描述                                                           |
| ------------ | -------------------------------------------------------------- |
| `text`       | 显示文本内容                                                   |
| `bitmap`     | 设置位图、内置error等                                          |
| `fg`         | 设置文字颜色                                                   |
| `bg`         | 设置背景颜色                                                   |
| `width`      | 设置宽度，未设置则适应内容                                     |
| `height`     | 设置高度，同上                                                 |
| `compund`    | 设置位图显示位置：left：图像居左、right、top、bottom、center、 |
| `wraplength` | 设置每行字符数，默认20                                         |
| `font`       | 设置字体大小                                                   |
| `relief`     | 制定的外观装饰边界附近的标签。默认是平的--                     |
| `justify`    | 制定多行的对齐方式                                             |
| `anchor`     | 指定文本或图像在Label中的显示位置                              |
| `padx`       | 文本左右两侧的空格数（默认为1）                                |
| `pady`       | 文本上下两侧的空格数（默认为1）                                |

[Label信息](https://jingyan.baidu.com/article/0320e2c1ebc3681b87507b2a.html)

#### 3.Frame
控件属性
| 参数                  | 描述                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| `bg`                  | 背景颜色                                                                                          |
| `bd`                  | 周围的边界的大小.默认为2像素.                                                                     |
| `curosr`              | 如果您将此选项设置为游标名称(箭头、点等)，则当游标位于checkbutton上方时，鼠标游标将更改为该模式。 |
| `font`                | 为新框架的垂直维度设置字体。                                                                      |
| `height`              | 垂直尺寸                                                                                          |
| `labelAnchor`         | 指定放置标签的位置                                                                                |
| `highlightbackground` | 高光背景,颜色的焦点突出时，帧没有焦点                                                             |
| `highlightcolor`      | 高光,颜色显示在焦点突出，当框架有焦点                                                             |
| `highlightthickness`  | 焦点的厚度                                                                                        |
| `relief`              | relief=FLAT, checkbutton在其后台不突出。您可以将此选项设置为其他任何样式                          |
| `text`                | 指定要在小部件中显示的字符串                                                                      |
| `width`               | 宽度                                                                                              |

#### 4. Entry
控件属性

| 参数   | 描述                                                                     |
| ------ | ------------------------------------------------------------------------ |
| height | 组件的高度（所占行数）                                                   |
| width  | 组件的宽度（所占字符个数）                                               |
| fg     | 前景字体颜色                                                             |
| bg     | 背景颜色                                                                 |
| show   | 将Entry框中的文本替换为指定字符，用于输入密码等，如设置 show="*"         |
| state  | 设置组件状态，默认为normal，可设置为：disabled—禁用组件，readonly—只读 |


[所有控件属性](http://www.eefocus.com/nightseas/blog/15-05/312601_ba94e.html)
### 几何管理方法
| 几何方法 | 描述 |
| -------- | ---- |
| pack()   | 包装 |
| grid()   | 网格 |
| place()  | 位置 |

### Variable类
有些控件 (比如 `Entry` 控件, `Radiobutton` 控件 等) 可以通过传入特定参数直接和一个程序变量绑定, 这些参数包括: `variable`, `textvariable`, `onvalue`, `offvalue`, `value`. 

这种绑定是双向的，及更改某一个另一个也随之更改。与python自带变量类似，但是不能够与变量直接传值

这些参数可接受的类型仅限于 Tkinter 包中的 `Variable` 类的子类. 如下:

```python
x = StringVar()    # 保存一个 string 类型变量, 默认值为""
x = IntVar()       # 保存一个整型变量, 默认值为0
x = DoubleVar()    # 保存一个浮点型变量, 默认值为0.0
x = BooleanVar()   # 保存一个布尔型变量, 返回值为 0 (代表 False) 或 1 (代表 True)
```

要得到其保存的变量值, 使用它的 get() 方法即可. 
要设置其保存的变量值, 使用它的 set() 方法即可.
