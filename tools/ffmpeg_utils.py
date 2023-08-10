from tools.download import download
from tools.uncompressed import unzip
import subprocess
import os

FFMPEG_BIN_PATH = 'ffmpeg/bin'


def ffmpeg_check(ffmpeg_bin_path=None):
    global FFMPEG_BIN_PATH
    if ffmpeg_bin_path is None:
        ffmpeg_bin_path = FFMPEG_BIN_PATH

    FFMPEG_BIN_PATH = os.path.abspath(ffmpeg_bin_path)
    if os.path.exists(os.path.join(FFMPEG_BIN_PATH, 'ffmpeg.exe')):
        print('ffmpeg 已经下载')
    else:
        url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip'
        file_name = 'ffmpeg.zip'
        if os.path.exists(file_name):
            os.remove(file_name)
        download(url, file_name)
        unzip(file_name)
        os.rename('ffmpeg-master-latest-win64-gpl-shared', 'ffmpeg')
        os.remove(file_name)


def ffmpeg_cmd(cmd_args):
    current_path = os.path.abspath(os.curdir)
    # print(current_path)
    os.chdir("../tools")
    ffmpeg_check()
    # print(os.path.abspath(os.curdir))
    os.chdir(current_path)
    # print(os.path.abspath(os.curdir))

    # cmd = 'SET PATH=%PATH%;"' + os.path.abspath(FFMPEG_BIN_PATH) + '" & ' + cmd
    cmd = '"' + os.path.abspath(os.path.join(FFMPEG_BIN_PATH, "ffmpeg.exe")) + '" ' + cmd_args
    print(cmd)
    result = os.popen(cmd)
    print(result.read())
    # result = system_call(cmd)
    # print(result)

    # print(cmd)
    # val = os.system(cmd)
    # if val == 0:
    #     print("Success")
    # else:
    #     print("Fail..")


def gen_mp4(image_file, audio_file, output_mp4_file):
    cmd = 'SET PATH=%PATH%;"' + FFMPEG_BIN_PATH + '" & '
    ffmpeg_cmd = 'ffmpeg -r 15 -loop 1 -i "' + image_file + '" -i "' + audio_file + \
                 '" -s 7680x3840 -pix_fmt yuvj420p -t 278 -vcodec libx264 "' + output_mp4_file + '"'
    print(ffmpeg_cmd)
    cmd = cmd + ffmpeg_cmd
