import requests
import logging
import os
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
font = FontProperties(fname=r"simsun.ttf", size=16)

# 使用说明：
# 1、访问 https://www.remove.bg/
# 2、注册帐号(Sign up)
# 3、填写 Email（电子邮箱）、Password（密码）、Password confirmation（确认密码）,保存
# 4、登录电子邮箱，点击“Activate Account” 激活帐号
# 5、登录 www.remove.bg，创建 API_KEY

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"


class RemoveBg:

    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def remove_background_from_img_file(self, img_file_path, size="regular"):
        """
        Removes the background given an image file and outputs the file as the original file name with "no_bg.png"
        appended to it.
        :param img_file_path: the path to the image file
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        """
        # Open image file to send information post request and send the post request
        img_file = open(img_file_path, 'rb')
        response = requests.post(
            API_ENDPOINT,
            files={'image_file': img_file},
            data={'size': size},
            headers={'X-Api-Key': self.__api_key})

        self.__output_file__(response, img_file.name + "_no_bg.png")

        # Close original file
        img_file.close()

    def remove_background_from_img_url(self, img_url, size="regular", new_file_name="no-bg.png"):
        """
        Removes the background given an image URL and outputs the file as the given new file name.
        :param img_url: the URL to the image
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param new_file_name: the new file name of the image with the background removed
        """
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_url': img_url,
                'size': size
            },
            headers={'X-Api-Key': self.__api_key}
        )
        self.__output_file__(response, new_file_name)

    def remove_background_from_base64_img(self, base64_img, size="regular", new_file_name="no-bg.png"):
        """
        Removes the background given a base64 image string and outputs the file as the given new file name.
        :param base64_img: the base64 image string
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param new_file_name: the new file name of the image with the background removed
        """
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_file_b64': base64_img,
                'size': size
            },
            headers={'X-Api-Key': self.__api_key}
        )
        self.__output_file__(response, new_file_name)

    def __output_file__(self, response, new_file_name):
        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            with open(new_file_name, 'wb') as removed_bg_file:
                removed_bg_file.write(response.content)
        # Otherwise, print out the error
        else:
            error_reason = response.json()["errors"][0]["title"].lower()
            logging.error("Unable to save %s due to %s", new_file_name, error_reason)


def mkdirs(dirs):
    for item in dirs:
        path = os.path.join(os.getcwd(), item)
        if not os.path.exists(path):  # 如果路径不存在
            os.makedirs(path)


def remove_bg(API_KEY, img_file, overwrite=False):
    """
    移除图片背景
    :param API_KEY: API_KEY 需要自己去注册 https://www.remove.bg
    :param img_file: 有背景的图片路径
    :param overwrite: 如果无背景图片已经存在，则直接返回文件路径，如果需要重新生成，请设置 overwrite=True
    :return:
    """
    # 构建无背景图片路径
    no_bg_file_name = img_file + "_no_bg.png"
    # 如果无背景图片已经存在，则直接返回文件路径，如果需要重新生成，请设置 overwrite=True
    if os.path.exists(no_bg_file_name) and not overwrite:
        print("%s 图片已经存在，如果需要重新生成，请设置 overwrite=True 或者删除该图片" % no_bg_file_name)
        return os.path.abspath(no_bg_file_name)
    # 出错的输出日志目录
    log_dir = "remove_bg_logs"
    mkdirs([log_dir])
    if API_KEY == "":
        raise Exception("使用前，请设置 API_KEY，需要自己去注册 https://www.remove.bg")
    # 图片的绝对路径
    img_file = os.path.abspath(img_file)
    print("正在调用 remove.bg API .....")
    # 构建 RemoveBg 类
    rmbg = RemoveBg(API_KEY,  # 引号内是你获取的API，需要自己去注册https://www.remove.bg/
                    os.path.join(log_dir, "error.log"))
    # 正在调用 remove.bg API .....
    rmbg.remove_background_from_img_file(img_file)
    print("调用结束")
    return os.path.abspath(no_bg_file_name)


def make_reg_photo(API_KEY, img_file, bg_color="red", out_dir="output"):
    """
    制作登记照（修改背景颜色）
    :param API_KEY: API_KEY 需要自己去注册 https://www.remove.bg
    :param img_file: 图片路径
    :param bg_color: 背景颜色：red、blue、white 或者元组 (R、G、B) 比如：(255, 0, 0)
    :param out_dir: 图片输出目录
    :return:
    """
    no_bg_file = img_file + "_no_bg.png"
    if not os.path.exists(no_bg_file):
        no_bg_file = remove_bg(API_KEY, img_file)
    else:
        pass
        # print("%s 去除背景的图片已经存在，如果需要重新生成，请删除该图片" % no_bg_file)

    mkdirs([os.path.abspath(out_dir)])
    bg_colors = {'red': (255, 0, 0),
                 'blue': (67, 142, 219),
                 'white': (255, 255, 255)}

    if type(bg_color) != tuple:
        _bg_color = bg_colors.get(bg_color, (255, 0, 0))
    else:
        _bg_color = bg_color
    img_file_name = os.path.basename(img_file)
    from PIL import Image
    im = Image.open(os.path.abspath(no_bg_file))  # 输入已经去除背景的图片
    x, y = im.size
    # 图片名称去掉扩展名
    img_file_name = "".join(img_file_name.split(".")[0:-1])
    # 构建输出图片文件路径
    out_img_file = os.path.join(out_dir, img_file_name + "_" + str(bg_color) + ".png")
    # 填充背景颜色
    p = Image.new('RGBA', im.size, _bg_color)
    p.paste(im, (0, 0, x, y), im)
    out_img_file = os.path.abspath(out_img_file)
    # 保存输出图片文件
    p.save(out_img_file)
    # 返回输出图片文件路径
    return out_img_file


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


if __name__ == '__main__':
    API_KEY = "" # API_KEY 需要自己去注册 https://www.remove.bg

    src_img = "images/cat_dog.jpg"
    show_img(src_img)  # 展示原始图片
    # 删除图片背景，no_bg_img_file 为图片路径
    no_bg_img_file = remove_bg(API_KEY, src_img)
    show_img(no_bg_img_file)  # 展示去除背景后的图片

    mm_img = "images/mm_02.jpg"
    show_img(mm_img)  # 展示原始图片
    # 处理为红色背景
    reg_photo_file = make_reg_photo(API_KEY, mm_img, bg_color="red")
    show_img(reg_photo_file, "红色背景")  # 展示处理后的登记照片

    # 处理为蓝色背景
    reg_photo_file = make_reg_photo(API_KEY, mm_img, bg_color="blue")
    show_img(reg_photo_file, "蓝色背景")  # 展示处理后的登记照片

    # 处理为白色背景
    reg_photo_file = make_reg_photo(API_KEY, mm_img, bg_color="white")
    show_img(reg_photo_file, "白色背景")  # 展示处理后的登记照片

    # 处理为RGB颜色的背景（黄色）
    reg_photo_file = make_reg_photo(API_KEY, mm_img, bg_color=(255, 255, 0))
    show_img(reg_photo_file, "黄色背景")  # 展示处理后的登记照片
