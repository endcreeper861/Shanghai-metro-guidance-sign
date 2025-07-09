import csv
from abc import ABC, abstractmethod
from math import ceil
from typing import Literal, NamedTuple, Union

from PIL import Image, ImageDraw, ImageFont

DEFAULT_FONT = "C:/Windows/Fonts/simhei.ttf"  # 黑体字体
DEFAULT_EN_FONT = "C:/Windows/Fonts/Arial.ttf"  # 英文字体

EXIT_COLOR = "#FFD10F"


ColorType = Union[float, tuple[int, ...], str]


class Size(NamedTuple):
    """尺寸类，用于存储宽度和高度"""

    width: int
    height: int


def get_color(line: int | str) -> tuple[str, str]:
    """
    根据线路编号或名称获取颜色。

    Args:
        line (int | str): 地铁线路的编号或名称。

    Returns:
        tuple[str, str]: 线路的颜色和文字颜色。
    """
    file = "colors.csv"
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if str(row["Line"]) == str(line):
                return row["BackgroundColor"], row["TextColor"]
    raise ValueError(f"未找到线路 {line} 的颜色信息，请检查 colors.csv 文件。")


class Element(ABC):
    """导向标识牌上的各个元素"""

    def __init__(self, size: int, color: ColorType = "white"):
        """
        初始化导向标识的元素。

        Args:
            size (int): 元素的大小。
            color (str): 元素的颜色，默认为白色。
        """
        self.size = size
        self.color = color

    @abstractmethod
    def get_size(self) -> Size:
        """
        获取元素的宽高。

        Returns:
            Size: 元素的宽度和高度。可以使用`width`和`height`属性访问。
        """
        pass

    @abstractmethod
    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
        """绘制元素。"""
        pass

    @property
    def width(self) -> int:
        """获取元素的宽度。"""
        return self.get_size().width

    @property
    def height(self) -> int:
        """获取元素的高度。"""
        return self.get_size().height


class Arrow(Element):
    """箭头"""

    def __init__(
        self,
        size: int,
        color: ColorType = "white",
        thickness: int | None = None,
        direction: Literal["up", "down", "left", "right"] = "left",
    ):
        """
        初始化箭头。

        Args:
            size (int): 箭头的大小。
            color (str): 箭头的颜色，默认为白色。
            thickness (int | None): 箭头的粗细，默认为 size 的四分之一。
            direction (Literal["up", "down", "left", "right"]): 箭头的方向，默认为向左。
        """
        super().__init__(size, color)
        if thickness is None:
            thickness = size // 4
        self.size = size
        self.thickness = thickness
        self.direction = direction
        self.color = color

    def get_size(self) -> Size:
        """
        获取箭头的宽高。

        Returns:
            Size: 箭头的宽度和高度。
        """
        return Size(self.size, self.size)

    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
        center_x = x + self.size // 2
        center_y = y + self.size // 2

        rect_1 = []
        rect_2 = []
        rectangle_coords = []

        if self.direction == "left":
            rect_1 = [
                (x, center_y),
                (x + self.thickness, center_y),
                (x + self.thickness + self.size // 3, center_y - self.size // 3),
                (x + self.size // 3, center_y - self.size // 3),
            ]
            rect_2 = [
                (x, center_y),
                (x + self.thickness, center_y),
                (x + self.thickness + self.size // 3, center_y + self.size // 3),
                (x + self.size // 3, center_y + self.size // 3),
            ]
            rectangle_coords = [
                (x + self.thickness // 2, center_y - self.thickness // 2.828),
                (x + self.size, center_y + self.thickness // 2.828),
            ]

        elif self.direction == "right":
            rect_1 = [
                (x + self.size, center_y),
                (x + self.size - self.thickness, center_y),
                (
                    x + self.size - self.thickness - self.size // 3,
                    center_y - self.size // 3,
                ),
                (x + self.size - self.size // 3, center_y - self.size // 3),
            ]
            rect_2 = [
                (x + self.size, center_y),
                (x + self.size - self.thickness, center_y),
                (
                    x + self.size - self.thickness - self.size // 3,
                    center_y + self.size // 3,
                ),
                (x + self.size - self.size // 3, center_y + self.size // 3),
            ]
            rectangle_coords = [
                (x, center_y - self.thickness // 2.828),
                (
                    x + self.size - self.thickness // 2,
                    center_y + self.thickness // 2.828,
                ),
            ]

        elif self.direction == "up":
            rect_1 = [
                (center_x, y),
                (center_x, y + self.thickness),
                (center_x - self.size // 3, y + self.thickness + self.size // 3),
                (center_x - self.size // 3, y + self.size // 3),
            ]
            rect_2 = [
                (center_x, y),
                (center_x, y + self.thickness),
                (center_x + self.size // 3, y + self.thickness + self.size // 3),
                (center_x + self.size // 3, y + self.size // 3),
            ]
            rectangle_coords = [
                (center_x - self.thickness // 2.828, y + self.thickness // 2),
                (center_x + self.thickness // 2.828, y + self.size),
            ]

        elif self.direction == "down":
            rect_1 = [
                (center_x, y + self.size),
                (center_x, y + self.size - self.thickness),
                (
                    center_x - self.size // 3,
                    y + self.size - self.thickness - self.size // 3,
                ),
                (center_x - self.size // 3, y + self.size - self.size // 3),
            ]
            rect_2 = [
                (center_x, y + self.size),
                (center_x, y + self.size - self.thickness),
                (
                    center_x + self.size // 3,
                    y + self.size - self.thickness - self.size // 3,
                ),
                (center_x + self.size // 3, y + self.size - self.size // 3),
            ]
            rectangle_coords = [
                (center_x - self.thickness // 2.828, y),
                (
                    center_x + self.thickness // 2.828,
                    y + self.size - self.thickness // 2,
                ),
            ]

        # 绘制箭头头的两个梯形
        draw.polygon(rect_1, fill=self.color)
        draw.polygon(rect_2, fill=self.color)

        # 绘制箭头柄的矩形
        draw.rectangle(rectangle_coords, fill=self.color)


class BilingualText(Element):
    """双语文本元素"""

    def __init__(
        self,
        size: int,
        text: str,
        text_en: str,
        color: ColorType = "white",
        align: Literal["left", "right"] = "left",
    ):
        """
        初始化文本元素。

        Args:
            size (int): 文本的大小。
            text (str): 中文文本。
            text_en (str): 英文文本。
            color (str): 文本颜色，默认为白色。
            align (Literal["left", "right"]): 文本对齐方式，默认为左对齐。
        """
        super().__init__(size, color)
        self.text = text
        self.text_en = text_en
        self.align = align
        self.font = ImageFont.truetype(DEFAULT_FONT, size // 1.5)
        self.en_font = ImageFont.truetype(DEFAULT_EN_FONT, size // 3)
        self.text_width = ceil(self.font.getbbox(self.text)[2])
        self.text_en_width = ceil(self.en_font.getbbox(self.text_en)[2])

    def get_size(self) -> Size:
        """获取文本的宽高。"""
        return Size(max(self.text_width, self.text_en_width), self.size)

    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
        """绘制文本。"""
        max_width = max(self.text_width, self.text_en_width)

        if self.align == "left":
            text_pos = (x, y)
            en_text_pos = (x + self.size // 30, y + self.size * 2 // 3)
        elif self.align == "right":
            text_pos = (x + max_width - self.text_width, y)
            en_text_pos = (
                x + max_width - self.text_en_width - self.size // 30,
                y + self.size * 2 // 3,
            )

        draw.text(
            text_pos,
            self.text,
            fill=self.color,
            font=self.font,
        )

        draw.text(
            en_text_pos,
            self.text_en,
            fill=self.color,
            font=self.en_font,
        )


class ExitSign(Element):
    """出口标识"""

    def __init__(self, size: int, code: str, color: ColorType = EXIT_COLOR):
        """
        初始化出口标识。

        Args:
            size (int): 标识的大小。
            color (str): 标识的颜色，默认为黄色。
        """
        super().__init__(size, color)
        self.text = BilingualText(
            size=size,
            text="出口",
            text_en="EXIT",
            color=color,
            align="right",
        )
        self.code = code
        self.font = ImageFont.truetype(DEFAULT_EN_FONT, size * 1.2)

    def get_size(self) -> Size:
        """获取出口标识的宽高。"""
        code_width = ceil(self.font.getbbox(self.code)[2])
        return Size(code_width + self.text.width, self.size)

    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
        """绘制出口标识。"""
        self.text.draw(draw, x, y)
        draw.text(
            (x + self.text.width, y - self.size // 8),
            self.code,
            fill=self.color,
            font=self.font,
        )


class NumberLine(Element):
    """数字线路标识"""

    def __init__(
        self,
        size: int,
        line: int | str | list[int | str],
        color: ColorType = "white",
    ):
        """ """
        if not isinstance(line, list):
            line = [line]

        self.lines = [str(l) for l in line]

        if not all(map(str.isdigit, self.lines)):
            raise ValueError("线路编号必须是数字。对于文本标签线路，请使用另一个函数。")

        self.text = BilingualText(
            size=size,
            text=f"号线",
            text_en=f"Line {",".join(self.lines)}",
            color=color,
        )

        super().__init__(size, color)

    def get_size(self) -> Size:
        """获取线路标识的宽高"""
        return Size(self.size * len(self.lines) + self.text.width, self.size)

    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int) -> None:

        for line in self.lines:
            line_color, line_text_color = get_color(line)
            # 第一步：画一个框
            # 计算边框宽度
            border_width = self.size // 30
            # 计算总高度，宽高比为 8.5:10
            box_width = round(self.size * 8.5 / 10)
            draw.rectangle(
                (x, y, x + box_width, y + self.size),
                fill=self.color,
                width=border_width,
            )
            draw.rectangle(
                (
                    x + border_width,
                    y + border_width,
                    x + box_width - border_width,
                    y + self.size - border_width,
                ),
                fill=line_color,
            )

            # 第二步：加上框内文字
            if len(line) == 1:
                font = ImageFont.truetype(DEFAULT_EN_FONT, self.size // 1.2)
            elif len(line) == 2:
                font = ImageFont.truetype(DEFAULT_EN_FONT, self.size // 1.5)
            else:
                raise ValueError("线路编号长度不支持超过2位数的线路。")
            # 计算文字宽度和高度
            width, height = font.getbbox(line)[2:]
            # 计算文字位置
            text_x = x + (box_width - width) // 2
            text_y = y + (self.size - height) // 2 - self.size // 15
            # 绘制文字
            draw.text((text_x, text_y), line, fill=line_text_color, font=font)

            x += self.size

        # 第三步：加上“号线”
        self.text.draw(draw, x, y)


class Sign:
    """地铁站导向标识牌"""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: ColorType = "black",
        padding: int | None = None,
    ) -> None:
        """
        初始化标识牌。

        Args:
            width (int): 标识牌的宽度。
            height (int): 标识牌的高度。
            background_color (ColorType): 标识牌的背景颜色，默认为黑色。
        """
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (width, height), background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.padding = padding if padding is not None else height // 12
        self.elements: list[tuple[Literal["left", "right", "middle"], Element]] = []

    def save(self, filename: str) -> None:
        """
        保存标识牌图像到文件。

        Args:
            filename (str): 保存的文件名。
        """
        left_elements = [e for align, e in self.elements if align == "left"]
        pos_x = self.padding
        pos_y = self.padding
        for element in left_elements:
            element.draw(self.draw, pos_x, pos_y)
            pos_x += element.width + self.padding

        middle_elements = [e for align, e in self.elements if align == "middle"]
        pos_x = (
            self.width
            - sum(e.width for e in middle_elements)
            - self.padding * (len(middle_elements) - 1)
        ) // 2
        for element in middle_elements:
            element.draw(self.draw, pos_x, pos_y)
            pos_x += element.width + self.padding

        right_elements = [e for align, e in self.elements if align == "right"]
        pos_x = self.width - self.padding
        for element in right_elements[::-1]:  # 从右向左绘制
            pos_x -= element.width
            element.draw(self.draw, pos_x, pos_y)
            pos_x -= self.padding

        self.image.save(filename)

    def add_element(
        self, element: Element, align: Literal["left", "right", "middle"] = "left"
    ) -> None:
        """
        添加元素到标识牌。

        Args:
            element (Element): 要添加的元素。
            align (Literal["left", "right", "middle"]): 元素的对齐方式，默认为左对齐。
        """
        self.elements.append((align, element))
