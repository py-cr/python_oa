# -*- coding: utf-8 -*-
# @Time    : 2022/8/1
# @Author  : Python超人
# @FileName: xlwt_ext.py

# xlwt 工具包可以对 xls 文件进行写操作
import xlwt


def create_style(back_color, font_color, font_size, horz, num_format_str="General"):
    """
    根据参数创建一个样式对象。
    样例：cell_style = create_style(back_color=57, font_color=1, font_size=12, horz=3)
    :param back_color: 背景颜色
    :param font_color: 字体颜色
    :param font_size: 字号
    :param horz: 水平对齐
                0: HORZ_GENERAL
                1: HORZ_LEFT
                2: HORZ_CENTER
                3: HORZ_RIGHT
                4: HORZ_FILLED
                5: HORZ_JUSTIFIED # BIFF4-BIFF8X
                6: HORZ_CENTER_ACROSS_SEL # Centred across selection (BIFF4-BIFF8X)
                7: HORZ_DISTRIBUTED # Distributed (BIFF8X)
    :param num_format_str: 单元格显示格式，可以不传值（默认=General）
    :return:
    """
    # 创建一个样式对象
    style = xlwt.XFStyle()

    # ================================================
    # 1.1 创建一个背景图案对象
    # 创建一个背景图案对象
    pattern = xlwt.Pattern()
    # 表示是否设置填充，默认 NO_PATTERN(值为0)，不设置任何填充。还有一个选项SOLID_PATTERN(1)，设置填充。
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # 设置填充的前景色赋值为黄色 ，参考：Excel颜色索引对照表
    pattern.pattern_fore_colour = back_color
    # 设置填充的背景色为蓝色，参考：Excel颜色索引对照表
    pattern.pattern_back_colour = back_color
    # ------------------------------------------------
    # 1.2 把背景图案加到样式里去
    style.pattern = pattern

    # ================================================
    # 2.1 创建字体
    font = xlwt.Font()
    # 设置字体
    font.name = '微软雅黑'
    # 设置字体颜色为红色，参考：Excel颜色索引对照表
    font.colour_index = font_color
    # 字体大小，font_size为字号，20为衡量单位
    font.height = 20 * font_size
    # ------------------------------------------------
    # 2.2 把字体加到样式里去
    style.font = font

    # ================================================
    # 3.1 创建对齐
    alignment = xlwt.Alignment()
    """
    # 水平对齐
    0: HORZ_GENERAL
    1: HORZ_LEFT
    2: HORZ_CENTER
    3: HORZ_RIGHT
    4: HORZ_FILLED
    5: HORZ_JUSTIFIED # BIFF4-BIFF8X
    6: HORZ_CENTER_ACROSS_SEL # Centred across selection (BIFF4-BIFF8X)
    7: HORZ_DISTRIBUTED # Distributed (BIFF8X)
    """
    alignment.horz = horz  # 水平对齐
    """
    垂直对齐
    0: VERT_TOP
    1: VERT_CENTER
    2: VERT_BOTTOM
    3: VERT_JUSTIFIED
    4: VERT_DISTRIBUTED
    """
    alignment.vert = 1  # 垂直对齐
    # 设置自动换行
    alignment.wrap = 1
    # ------------------------------------------------
    # 3.2 把对齐加到样式里去
    style.alignment = alignment

    # ================================================
    # 4.1 创建边框
    borders = xlwt.Borders()
    # 设置上下左右边框为虚线
    # DASHED为虚线 、NO_LINE 为没有边框、THIN 为实线
    borders.top = xlwt.Borders.DASHED
    borders.bottom = xlwt.Borders.DASHED
    borders.left = xlwt.Borders.DASHED
    borders.right = xlwt.Borders.DASHED

    # 设置上下左右边框为颜色为蓝色
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0

    # 设置上下左右边框线型和粗细
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    # 4.2 把边框加到样式里去
    style.borders = borders

    # ================================================
    # 5 单元格显示格式
    style.num_format_str = num_format_str

    # 把样式对象返回给变量，比如：
    # cell_style = create_style(back_color=57, font_color=1, font_size=12, horz=3)
    # 变量 cell_style 就是 这个返回样式对象，我们称为返回值
    return style
