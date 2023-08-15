import sys
import os

sys.path.append("..")
from tools.ffmpeg_utils import ffmpeg_cmd

from datetime import datetime, timedelta


# def time_to_seconds(t):
#     if not isinstance(t, str):
#         return t
#
#     if t.find('.') == -1:
#         t = t + ".0"
#
#     # 解析时间字符串为datetime对象
#     time_obj = datetime.strptime(t, "%H:%M:%S.%f")
#     # 计算总秒数
#     total_seconds = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second,
#                               microseconds=time_obj.microsecond).total_seconds()
#
#     return total_seconds
#
#
# # 测试
# print(time_to_seconds('00:01:02'))  # 输出62.0
# print(time_to_seconds('01:02:03'))  # 输出3723.0
# print(time_to_seconds('01:02:03.123'))  # 输出3723.123
# print(time_to_seconds('00:02:03.123'))  # 输出123.123


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


def trim_audio(input_file, start_time, end_time,
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

    start_time = time_to_seconds(start_time)
    end_time = time_to_seconds(end_time)
    afade = ""
    if fade_in_duration > 0:
        afade = f"afade=t=in:ss=0:d={fade_in_duration}"

    if fade_out_duration > 0:
        if len(afade) > 0:
            afade = afade + ","

        afade = afade + f"afade=t=out:st={end_time - start_time - fade_out_duration}:d={fade_out_duration}"

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


# 测试
# print(time_to_seconds('01:02'))  # 输出62.0
# print(time_to_seconds('01:02:03'))  # 输出3723.0
# print(time_to_seconds('01:02:03.123'))  # 输出3723.123
# print(time_to_seconds('02:03.123'))  # 输出123.123
# print(time_to_seconds('03.123'))  # 输出3.123

if __name__ == '__main__':
    # 示例用法
    input_file = 'audio/dein_weg.mp3'  # 输入音频文件
    output_file = 'dein_weg_phone.mp3'  # 输出音频文件
    output_file = None
    start_time = '00:00:11.5'  # 起始时间（单位：秒）
    end_time = '00:00:21.5'  # 结束时间（单位：秒）

    trim_audio(input_file=input_file,
               start_time=start_time, end_time=end_time,
               output_file=output_file,
               fade_in_duration=3, fade_out_duration=5)
