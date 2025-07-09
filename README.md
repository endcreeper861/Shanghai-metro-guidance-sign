# 上海地铁风格导向标识生成器

## 介绍

这是一个用于生成上海地铁风格导向标识的 Python 库。它使用了 `Pillow` 库来处理图像，并提供了多种元素和大量可自定义的参数来创建自定义的导向标识。

导向标识参考了《DB31/T 1104-2018 城市轨道交通导向标识系统设计规范》，但并非完全遵守。

## 功能特点

- 生成数字线路标识（带线路颜色）
- 创建四种方向的箭头指示
- 添加中英双语文本
- 生成出口标识（与出口编号）
- 组合多个元素创建完整的导向标识牌
- 自定义尺寸、颜色和对齐方式

## 如何使用

首先确保你已经安装了 `Pillow` 库：

```bash
pip install Pillow
```

将 `sign.py` 文件放在你的项目目录中，然后使用以下代码来生成导向标识：

```python
from sign import Sign, NumberLine, Arrow, BilingualText

# 创建基础标识牌（宽512像素，高128像素）
sign = Sign(512, 128)

# 添加3号线标识
sign.add_element(NumberLine(108, 3))

# 添加向右的箭头
sign.add_element(Arrow(108, direction="right"))

# 保存为PNG图像
sign.save("line_3_right.png")
```

之后可以在当前目录下找到生成的 `line_3_right.png` 文件。像这样：

![line_3_right](line_3_right.png)

更多示例可参考 `example.py` 文件。

![platform_sign](platform_sign.png)
![century_avenue_sign](century_avenue.png)
![exit_sign](exit_sign.png)
![airport_link_line](airport_link_line.png)

## 颜色配置文件

项目使用 `colors.csv` 文件存储线路颜色信息，格式如下：

```csv
Line,BackgroundColor,TextColor
1,#E4002B,white
2,#97D700,white
3,#FFD100,black
...
```
