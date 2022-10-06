from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
font = FontProperties(fname=r"simsun.ttf", size=16)


def show_img(image_file, title=None):
    """
    显示图片的函数
    """
    from PIL import Image
    plt.figure('image', figsize=(8, 6))
    plt.xticks([])
    plt.yticks([])
    im = Image.open(image_file)
    plt.imshow(im)
    if title is not None:
        plt.title(title)
    plt.show()
