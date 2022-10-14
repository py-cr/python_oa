# -*- coding: utf-8 -*-
# @Time    : 2022/10/06 15:30
# @Author  : Python超人
# @FileName: img_utils.py

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl
import tinify
import os


mpl.rcParams['font.sans-serif'] = ['SimHei']
font = FontProperties(fname=r"simsun.ttf", size=16)


def show_img(image_file, title=None, figsize=(8, 6)):
    """
    显示图片的函数
    """
    from PIL import Image
    plt.figure('image', figsize=figsize)
    plt.xticks([])
    plt.yticks([])
    im = Image.open(image_file)
    plt.imshow(im)
    if title is not None:
        plt.title(title)
    plt.show()


def compress_image(api_key, source_file, output_file):
    """
    压缩文件
    :param api_key: API_KEY
    :param source_file: 原始图片路径
    :param output_file: 压缩后图片路径
    :return:
    """
    tinify.key = api_key
    source = tinify.tinify.from_file(source_file)
    result = source.to_file(output_file)
    if result:
        print(result)