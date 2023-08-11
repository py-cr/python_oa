from PIL import Image
import sys
import os

sys.path.append("..")
from tools.ffmpeg_utils import ffmpeg_cmd


#     1   2   3   4
#   ┌───┬───┬───┬───┐
# 1 │   │ u │   │   │
#   ├───┼───┼───┼───┤
# 2 │ l │ f │ r │ b │
#   ├───┼───┼───┼───┤
# 3 │   │ d │   │   │
#   └───┴───┴───┴───┘

def conv_to_cubemap_6x1(src_image, col_num=4, row_num=3,
                        rludfb=[(3, 2), (1, 2), (2, 1), (2, 3), (2, 2), (4, 2)]):
    # Open the panoramic image
    panoramic_image = Image.open(src_image)
    # Get the width and height of the panoramic image
    width, height = panoramic_image.size
    # Calculate the dimensions of each cubemap face
    face_width = width // col_num
    face_height = height // row_num
    # Create a new blank cubemap image with the desired dimensions
    cubemap_image = Image.new('RGB', (face_width * 6, face_height))

    for idx, (col_idx, row_idx) in enumerate(rludfb):
        cubemap_image.paste(panoramic_image.crop((face_width * (col_idx - 1),
                                                  face_height * (row_idx - 1),
                                                  face_width * col_idx,
                                                  face_height * row_idx)),
                            (face_width * idx, 0))

    cubemap_6x1 = src_image[0:-4] + "_6x1.png"
    # Return the cubemap image
    cubemap_image.save(cubemap_6x1)
    return cubemap_6x1


def cubemap_6x1_to_panorama(cubemap_6x1_image, output_image):
    """
    cubemap 6x1 转全景图片
    @param cubemap_6x1_image:
    @param output_image:
    @return:
    """
    dirname = os.path.dirname(output_image)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    ffmpeg_cmd(f'-i "{cubemap_6x1_image}" -y -vf v360=c6x1:e:cubic:in_forder="rludfb" "{output_image}"')
    return output_image


def conv_to_panoramic_video(panoramic_image, audio_file, output_mp4, size="1920x1080", rate=1):
    """
    将一张全景图片、音频合成一个 mp4视频文件
    @param panoramic_image: 全景图片
    @param audio_file: 音频文件
    @param output_mp4: 输出的mp4视频文件名
    @param size: 输出的分辨率：
                1K分辨率：1920*1080
                2K分辨率：2048×1080
                4K分辨率：4096×2160
                8K分辨率：7680x4320
    @param rate:
    @return:
    """
    cmd = f' -r {rate} -i "{panoramic_image}" -i "{audio_file}" ' \
          f'-s {size} -pix_fmt yuvj420p -t 278 -vcodec libx264 "{output_mp4}"'
    ffmpeg_cmd(cmd)
    return output_mp4
