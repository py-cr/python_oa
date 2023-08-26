import sys
import os
import math

sys.path.append("..")
from tools.ffmpeg_utils import ffmpeg_cmd

from datetime import datetime, timedelta

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


def show_imgs(images, titles=[], rows=3, cols=3, figsize=(18, 16)):
    from PIL import Image

    if titles is None:
        titles = []

    if len(titles) == 0:
        titles = images

    from matplotlib import pyplot as plt
    plt.figure('image', figsize=figsize)
    for i in range(len(images)):
        image_file = images[i]
        if i <= len(titles) - 1:
            title = titles[i]
        else:
            title = None
        if isinstance(image_file, str):
            im = Image.open(image_file)
            if title is None:
                title = image_file
        else:
            im = image_file
        plt.subplot(rows, cols, i + 1), plt.imshow(im)
        if title is None:
            title = "image:%s" % (i)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
    plt.show()


def show_imgs(images, titles=[], rows=3, cols=3, figsize=(8, 6),
              left=0.03, bottom=0.03, right=0.97, top=0.97, wspace=0.05, hspace=0.05
              # left=0, bottom=0, right=1, top=0.9,wspace=-0.2, hspace=0.2
              ):
    from PIL import Image
    from matplotlib import pyplot as plt

    # 如果titles为空，则使用images作为titles
    if titles is None:
        titles = []
    if len(titles) == 0:
        titles = images

    # 创建一个figure对象，并设置大小
    fig = plt.figure('image', figsize=figsize)

    # left=None, bottom=None, right=None, top=None,wspace=-0.2, hspace=-0.5
    # 调整子图之间的间距
    fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    # 遍历所有图片，并显示在子图中
    for i in range(len(images)):
        image_file = images[i]
        # 如果titles中有对应的标题，则使用该标题
        if i <= len(titles) - 1:
            title = titles[i]
        else:
            title = None
        if isinstance(image_file, str):
            im = Image.open(image_file)
            if title is None:
                title = image_file
        else:
            im = image_file
        # 在第i+1个子图中显示该图片
        ax = fig.add_subplot(rows, cols, i + 1)
        ax.imshow(im)
        if title is None:
            title = "image:%s" % (i)
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()


def makedirs(file_path):
    dirname = os.path.dirname(file_path)
    if len(dirname) > 0 and not os.path.exists(dirname):
        os.makedirs(dirname)


def time_to_seconds(t):
    if not isinstance(t, str):
        return t

    time_parts = t.split(':')
    if len(time_parts) == 2:  # 分钟:秒
        minutes, seconds = map(float, time_parts)
        return minutes * 60 + seconds
    elif len(time_parts) == 3:  # 小时:分钟:秒 或 小时:分钟:秒.毫秒
        hours, minutes, seconds = map(float, time_parts)
        if '.' in str(seconds):  # 小时:分钟:秒.毫秒
            seconds_parts = str(seconds).split('.')
            seconds = float(seconds_parts[0])
            milliseconds = float(seconds_parts[1])
            return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        else:  # 小时:分钟:秒
            return hours * 3600 + minutes * 60 + seconds
    elif len(time_parts) == 1:  # 分钟:秒.毫秒
        # minutes, seconds = map(float, time_parts[0].split('.'))
        # return minutes * 60 + seconds / 1000
        return float(t)
    else:
        raise ValueError("Invalid time format")


def av_trim(input_file, start_time, end_time,
            output_file: str = None,
            volume=1.0,
            fade_in_duration=0,
            fade_out_duration=0):
    """
    对音频进行片段截取的功能
    @param input_file: 音频文件路径
    @param start_time: 截取的开始时间
    @param end_time: 截取的结束时间
    @param output_file: 输出的文件
    @param volume: 控制音量
    @param fade_in_duration: 音频渐入时长（单位：秒）
    @param fade_out_duration: 音频渐出时长（单位：秒）
    @return:
    """

    if output_file is None:
        p = input_file.rfind(".")

        output_file = input_file[0:p] + "_out" + input_file[p:]

    makedirs(output_file)

    start_time = time_to_seconds(start_time)
    end_time = time_to_seconds(end_time)
    afade = ""
    if fade_in_duration > 0:
        afade = f"afade=t=in:ss=0:d={fade_in_duration}"

    if fade_out_duration > 0:
        if len(afade) > 0:
            afade = afade + ","
        st = round(end_time - start_time - fade_out_duration, 2)
        afade = afade + f"afade=t=out:st={st}:d={fade_out_duration}"

    if volume != 1.0:
        if len(afade) > 0:
            afade = afade + ","
        afade = afade + f"volume={volume}"

    if len(afade) > 0:
        afade = ' -af "' + afade + '"'
        p = output_file.rfind(".")
        tmp_file = output_file[0:p] + "_tmp" + output_file[p:]
    else:
        tmp_file = output_file

    ffmpeg_cmd(f'-i "{input_file}" -y -c copy -ss {start_time} -to {end_time} "{tmp_file}"')

    if len(afade) > 0:
        ffmpeg_cmd(f'-i "{tmp_file}" -y {afade} "{output_file}"')
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

    return output_file


def v_to_mp3(video_file, output_mp3_file):
    makedirs(output_mp3_file)
    # ffmpeg
    ffmpeg_cmd(f' -y -i "{video_file}" -vn -acodec libmp3lame "{output_mp3_file}"')
    return output_mp3_file


def ia_to_mp4(image_files, audio_file, output_mp4_file):
    if isinstance(image_files, list) and len(image_files) == 1:
        image_files = image_files[0]

    if isinstance(image_files, list):
        duration = get_duration(audio_file)
        cmd = " -y "
        vn = ""
        filter_complex = ''
        images_len = len(image_files)
        # 计算每张图片的显示的时间长度
        setpt = duration / images_len
        setpt = round(math.ceil(setpt * 1000) / 1000, 3)
        # if not isinstance(setpts, list):
        #     setpts = [setpts] * images_len

        for i, image_file in enumerate(image_files):
            cmd += f' -loop 1 -t {setpt} -i "{image_file}" '
            # cmd += f' -loop 1 -i "{image_file}" '
            # filter_complex += f'[{i}:v]setpts=PTS+{setpts[i]}/TB[v{i}];'
            filter_complex += f'[{i}:v]setpts=1*PTS[v{i}];'
            # [0:v]setpts=3*PTS[v0]
            vn += f"[v{i}]"
        filter_complex += f'{vn}concat=n={images_len}:v=1:a=0[v]'
        cmd += f' -i "{audio_file}" '
        cmd += f' -filter_complex "{filter_complex}"'
        cmd += f' -map "[v]" -map {images_len}:a -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p "{output_mp4_file}"'
    else:
        cmd = f' -y -loop 1 -i "{image_files}" -i "{audio_file}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{output_mp4_file}"'

    ffmpeg_cmd(cmd)

    # ffmpeg -loop 1 -t 3.5 -i image1.jpg -loop 1 -t 2.5 -i image2.jpg -i audio.mp3
    # -filter_complex "[0:v]setpts=PTS+3.5/TB[v0];[1:v]setpts=PTS+2.5/TB[v1];[v0][v1]concat=n=2:v=1:a=0:loop=1[v]" -map "[v]"
    # -map 2:a -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p output.mp4

    # ffmpeg  -i image1.jpg -loop 1 -i image2.jpg -loop 1 -i image3.jpg
    # -i audio.mp3
    # -filter_complex "[0:v]setpts=3*PTS[v0];[1:v]setpts=3*PTS[v1];[2:v]setpts=3*PTS[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]"
    # -map "[v]" -map 3:a -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p output.mp4

    # ffmpeg -loop 1 -t 5.5 -i image1.jpg -loop 1 -t 5.5 -i image2.jpg -loop 1 -t 5.5 -i image3.jpg
    # -i audio.mp3 -filter_complex
    # "[0:v]setpts=PTS+5.5/TB[v0];[1:v]setpts=PTS+5.5/TB[v1];[2:v]setpts=PTS+5.5/TB[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]"
    # -map "[v]" -map 3:a -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p output.mp4

    # ffmpeg -loop 1 -t 5.5 -i image1.jpg -loop 1 -t 5.5 -i image2.jpg
    # -i audio.mp3 -filter_complex
    # "[0:v]setpts=PTS+5.5/TB[v0];[1:v]setpts=PTS+5.5/TB[v1];[v0][v1]concat=n=2:v=1:a=0[v]"
    # -map "[v]" -map 2:a -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p output.mp4

    # ffmpeg
    pass


def get_duration(file):
    import re
    pattern = "Duration: (.*?), start: (.*?), bitrate: (\\d*) kb\\/s"
    output = ffmpeg_cmd(f' -i "{file}"')
    result = re.findall(pattern=pattern, string=output)

    if len(result) > 0:
        duration = time_to_seconds(result[0][0]) + float(result[0][1])
    return duration


def picture_in_picture(image_file, video_file, pos_start, pos_end, output_file=None):
    """
    实现画中画
    :param image_file: 图片
    :param video_file: 画中画的视频文件
    :param pos_start: 画中画开始位置
    :param pos_end: 画中画结束位置
    :param output_file: 输出视频文件
    :return:
    """
    pos_x, pos_y, width, height = pos_start[0], pos_start[1], pos_end[0] - pos_start[0], pos_end[1] - pos_start[1]

    if output_file is None:
        p = video_file.rfind(".")
        output_file = video_file[:p] + "_pip" + video_file[p:]
    ffmpeg_cmd(
        f' -y -r 15 -i "{image_file}" -i "{video_file}" -filter_complex "[1:v]scale=w={width}:h={height} '
        f' [ovrl]; [0:v][ovrl] overlay=x={pos_x}:y={pos_y}" -pix_fmt yuvj420p -t 278 -vcodec libx264 "{output_file}"')


def cubemap_6x1_to_panorama(cubemap_6x1_image, output_image, in_forder="rludfb"):
    """
    cubemap 6x1 转全景图片
    @param cubemap_6x1_image:
    @param output_image:
    @param in_forder: 默认：rludfb
    @return:
    """
    dirname = os.path.dirname(output_image)
    if len(dirname) > 0 and not os.path.exists(dirname):
        os.makedirs(dirname)

    ffmpeg_cmd(f'-i "{cubemap_6x1_image}" -y -vf v360=c6x1:e:cubic:in_forder="{in_forder}" "{output_image}"')
    return output_image


# 测试
# print(time_to_seconds('01:02'))  # 输出62.0
# print(time_to_seconds('01:02:03'))  # 输出3723.0
# print(time_to_seconds('01:02:03.123'))  # 输出3723.123
# print(time_to_seconds('02:03.123'))  # 输出123.123
# print(time_to_seconds('03.123'))  # 输出3.123

if __name__ == '__main__':
    # 示例用法
    # input_file = 'audio/dein_weg.mp3'  # 输入音频文件
    # output_file = 'dein_weg_phone.mp3'  # 输出音频文件
    # output_file = None
    # start_time = '00:00:11.5'  # 起始时间（单位：秒）
    # end_time = '00:00:21.5'  # 结束时间（单位：秒）
    #
    # av_trim(input_file=input_file,
    #         start_time=start_time, end_time=end_time,
    #         output_file=output_file,
    #         fade_in_duration=3, fade_out_duration=5)
    # print(get_duration('output/少年_片段.mp3'))
    # ia2mp4(['images/magazine_1.jpg', 'images/magazine_2.jpg', 'images/magazine_3.jpg'],
    #        'output/少年_片段.mp3',
    #        'output/magazine.mp4'
    #        )
    show_imgs(["images/cat.jpg", "images/duck.jpg", "images/bear.jpg"], cols=3, rows=1)
