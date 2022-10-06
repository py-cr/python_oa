# -*- coding: utf-8 -*-
# @Time    : 2022/10/06 15:30
# @Author  : Python超人
# @FileName: watermarker.py

from PIL import Image, ImageDraw, ImageFont
import os


def add_water_marker_text_to_image(src_image,
                                   out_image,
                                   text,
                                   alpha=50,
                                   rotate=-45,
                                   font_file="msyh.ttc",
                                   font_size=50,
                                   h_density=1,
                                   v_density=1):
    """
    增加文字水印到图片
    :param src_image: 原始图片路径
    :param out_image: 增加水印后的图片路径
    :param text: 增加水印文字内容
    :param alpha: 透明度 0 - 255，默认：50
    :param rotate: 旋转角度，默认：-45度
    :param font_file: 字体文件，默认：微软雅黑
        # msyh.ttc  msyhbd.ttc  msyhl.ttc 微软雅黑
        # stxingka.ttf 华文行楷   simkai.ttf 楷体  simli.ttf隶书
        # minijianhuangcao.ttf  迷你狂草
        # kongxincaoti.ttf 空心草
    :param font_size: 字号大小，默认：50
    :param h_density: 文字水平疏密程度，默认：1，越大越密
    :param v_density: 文字垂直疏密程度，默认：1，越大越密
    :return:
    """
    # 如果为字符串，则认为是图片文件路径，如果文件存在则读取到图片
    if type(src_image) is str:
        if os.path.exists(src_image):
            src_image = Image.open(src_image)

    # 如果没有找到字体文件
    if not os.path.exists(font_file):
        # 如果字体文件不包含路径，则加入window默认字体路径
        if not (font_file.__contains__("\\") or font_file.__contains__("/")):
            font_file = 'C:\\Windows\\Fonts\\' + font_file

        if not os.path.exists(font_file):
            print("没有找到字体文件 %s" % font_file)
            # 如果字体文件不存在，则使用默认字体（微软雅黑）
            font_file = 'C:\\Windows\\Fonts\\msyh.ttc'
    # 读取字体
    font = ImageFont.truetype(font_file, font_size)  #

    # 添加背景
    new_img = Image.new('RGBA', (src_image.size[0] * 3, src_image.size[1] * 3), (0, 0, 0, 0))
    new_img.paste(src_image, src_image.size)

    # 添加水印
    font_len = len(text)
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    for i in range(0, rgba_image.size[0], int((font_len * 40 + 100) / h_density)):
        for j in range(0, rgba_image.size[1], int(200 / v_density)):
            image_draw.text((i, j), text, font=font, fill=(0, 0, 0, alpha))

    text_overlay = text_overlay.rotate(rotate)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    # 裁切图片
    image_with_text = image_with_text.crop(
        (src_image.size[0], src_image.size[1], src_image.size[0] * 2, src_image.size[1] * 2))

    image_with_text.save(out_image)
    del image_draw  # 删除画笔
    image_with_text.close()  # 关闭图片


if __name__ == '__main__':
    add_water_marker_text_to_image(
        src_image="01.png",
        out_image=u'Python超人_水印.png',
        text=u'Python超人',
        alpha=50,
        rotate=-45,
        # font_file="msyh.ttc",
        font_file="simli.ttf",
        font_size=40,
        h_density=1.5,
        v_density=1.5)
