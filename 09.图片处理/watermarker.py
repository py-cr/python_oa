# -*- coding: utf-8 -*-
# @Time    : 2022/10/06 15:30
# @Author  : Python超人
# @FileName: water_marker.py

from PIL import Image, ImageDraw, ImageFont
import os


def add_water_marker_text_to_image(src_image,
                                   out_image,
                                   text,
                                   alpha=0.8,
                                   rotate=-45,
                                   font_file="msyh.ttc",
                                   font_size=50,
                                   h_density=1,
                                   v_density=1):
    """
    增加文字水印到图片
    :param src_image: 原始图片路径
    :param out_image: 增加文字水印后的图片保存路径
    :param text: 增加水印文字内容
    :param alpha: 透明度 0 - 1，默认：0.8
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
    alpha = int(255 * alpha)
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
    if out_image is not None:
        out_dir = os.path.dirname(out_image)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        image_with_text.save(out_image)
        # del image_draw  # 删除画笔
        # image_with_text.close()  # 关闭图片
        print("水印添加成功：%s" % out_image)
    return image_with_text


def add_water_marker_logo_to_image(src_image, out_image, logo_image, alpha=0.8, rotate=0, logo_scale=0.5,
                                   position="bottomright"):
    """
    增加Logo图片水印到图片
    :param src_image: 原始图片路径
    :param out_image: 增加Logo水印后的图片保存路径
    :param logo_image: Logo图片路径
    :param alpha: 透明度 0 - 1，默认：0.8
    :param rotate: 旋转角度，默认：0
    @param logo_scale: Logo图片缩放，1为原尺寸，默认为 0.5
    @param position: Logo水印的位置，比如：(10,200)，并支持九种布局方式，分别是topleft、topmiddle、topright、middleleft、middlecenter、middleright、bottomleft、bottommiddle和bottomright
    @return:
    """
    alpha = int(255 * alpha)
    src = Image.open(src_image).convert('RGBA')  # 打开原文件
    logo = Image.open(logo_image).convert("RGBA")

    logo_x, logo_y = logo.size  # 获得长和宽

    # 设置每个像素点颜色的透明度
    for i in range(logo_x):
        for k in range(logo_y):
            color = logo.getpixel((i, k))
            if color[3] > 0:
                color = color[:-1] + (alpha,)
            logo.putpixel((i, k), color)

    # 缩放图片
    logo_scale_width = int(logo.size[0] * logo_scale)
    logo_scale_height = int(logo.size[1] * logo_scale)
    logo = logo.resize((logo_scale_width, logo_scale_height))  # 打开并转换设置logo水印
    # 旋转图片
    logo = logo.rotate(-rotate)
    src_width, src_height = src.size
    logo_width, logo_height = logo.size
    # 位置布局定义字典，大家可以在这里扩展
    position_dict = {
        "topleft": lambda: (0, 0),
        "topmiddle": lambda: (int((src_width - logo_width) / 2), 0),
        "topright": lambda: (src_width - logo_width, 0),
        "middleleft": lambda: (0, int((src_height - logo_height) / 2)),
        "middlecenter": lambda: (int((src_width - logo_width) / 2), int((src_height - logo_height) / 2)),
        "middleright": lambda: (src_width - logo_width, int((src_height - logo_height) / 2)),
        "bottomleft": lambda: (0, src_height - logo_height),
        "bottommiddle": lambda: (int((src_width - logo_width) / 2), src_height - logo_height),
        "bottomright": lambda: (src_width - logo_width, src_height - logo_height)
    }
    # position 为字符串类，则使用 position_dict 位置布局定义字典
    if type(position) == str:
        position = position_dict.get(position, (src_width - logo_width, src_height - logo_height))()
    elif type(position) == tuple or type(position) == list:  # 如果为元组或者数组，例如： (10, 100) 或者 [0, 100]
        if len(position) != 2:
            error_msg = "position 长度应该为2，例如： (10, 100) 或者 [0, 100]，实际为：%s" % position
            raise Exception(error_msg)
    else:
        error_msg = "position 必须为位置值，比如：元组(10，200)，或者指定如下布局方式 \ntopleft、topmiddle、topright、middleleft、middlecenter、middleright、bottomleft、bottommiddle、bottomright"
        raise Exception(error_msg)

    image_with_logo = Image.new('RGBA', (src_width, src_height), (0, 0, 0, 0))  # 创建新图像：透明
    image_with_logo.paste(src, (0, 0))
    print("position =", position)
    image_with_logo.paste(logo, position, mask=logo)
    # image_with_logo.show()
    if out_image is not None:
        out_dir = os.path.dirname(out_image)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        image_with_logo.save(out_image)
    print("水印添加成功：%s" % out_image)

    return image_with_logo


if __name__ == '__main__':
    from img_utils import show_img

    # 增加水印后的图片路径
    # 原始图片路径
    src_image = "./images/cat_dog.jpg"
    out_image = './output/图片加Logo水印.png'
    logo_image = './images/cat_dog.jpg'
    logo_image = './images/python_icon.png'

    add_water_marker_logo_to_image(
        src_image=src_image,
        out_image=out_image,
        logo_image=logo_image,
        alpha=1,
        rotate=0,
        logo_scale=0.5,
        position=(10, 200)
    ).show()
    show_img(out_image, "添加水印")
    # add_water_marker_text_to_image(
    #     src_image="01.png",
    #     out_image=u'Python超人_水印.png',
    #     text=u'Python超人',
    #     alpha=50,
    #     rotate=-45,
    #     # font_file="msyh.ttc",
    #     font_file="simli.ttf",
    #     font_size=40,
    #     h_density=1.5,
    #     v_density=1.5)
