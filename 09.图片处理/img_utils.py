# -*- coding: utf-8 -*-
# @Time    : 2022/10/06 15:30
# @Author  : Python超人
# @FileName: img_utils.py

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl

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
    if isinstance(image_file, str):
        im = Image.open(image_file)
    else:
        im = image_file
    plt.imshow(im)
    if title is not None:
        plt.title(title)
    plt.show()
