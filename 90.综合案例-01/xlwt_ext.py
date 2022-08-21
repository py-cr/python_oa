# -*- coding: utf-8 -*-
# @Time    : 2022/4/23 15:30
# @Author  : Python超人
# @FileName: xlwt_ext.py

# xlwt 工具包可以对 xls 文件进行写操作
# xlwt 的命名是 excel writer 简写，很容易记忆
import xlwt


def create_style(back_color):
    """
    创建一个样式功能函数，并返回
    :return:
    """
    # 创建一个样式对象
    style = xlwt.XFStyle()

    # 创建一个背景图案对象
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = back_color
    pattern.pattern_back_colour = back_color

    # 把背景图案加到样式里去
    style.pattern = pattern

    # 创建字体
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.colour_index = 2
    font.height = 20 * 16

    # 把字体加到样式里去
    style.font = font

    # 创建对齐
    alignment = xlwt.Alignment()
    alignment.horz = 2  # 居中
    alignment.vert = 1
    # 设置自动换行
    alignment.wrap = 1

    # 把对齐加到样式里去
    style.alignment = alignment

    # 创建边框
    borders = xlwt.Borders()
    # 设置上下左右边框为虚线
    # DASHED为虚线 、NO_LINE 为没有边框、THIN 为实线
    borders.top = xlwt.Borders.DASHED
    borders.bottom = xlwt.Borders.DASHED
    borders.left = xlwt.Borders.DASHED
    borders.right = xlwt.Borders.DASHED

    # 设置上下左右边框为颜色为蓝色
    borders.left_colour = 4
    borders.right_colour = 4
    borders.top_colour = 4
    borders.bottom_colour = 4

    # 设置上下左右边框线型和粗细
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    # 把边框加到样式里去
    style.borders = borders
    return style
