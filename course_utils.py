# -*- coding:utf-8 -*-
# filename        :course_utils.py
# description     :课程工具类
# author          :Python超人
# date            :2022/8/25
# notes           :
# ==============================================================================

import requests
import datetime
import time
import os
import zipfile
import shutil


def force_merge_flat_dir(src_dir, dst_dir):
    """

    @param src_dir: 来源目录
    @param dst_dir: 目标目录
    @return:
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for item in os.listdir(src_dir):
        src_file = os.path.join(src_dir, item)
        dst_file = os.path.join(dst_dir, item)
        force_copy_file(src_file, dst_file)


def force_copy_file(sfile, dfile):
    """
    强制复制文件
    @param sfile: 源文件
    @param dfile: 目标文件
    @return:
    """
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)


def contains_sub_dir(s_dir):
    """
    指定目录是否包含子目录
    @param s_dir: 指定目录
    @return:
    """
    for item in os.listdir(s_dir):
        s_item = os.path.join(s_dir, item)
        if os.path.isdir(s_item):
            return True
    return False


def _copy_files(src, dst):
    """
    复制指定目录的文件到另外一个目录
    @param src: 源目录
    @param dst: 目标目录
    @return:
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            if not os.path.exists(dst):
                os.makedirs(dst)
            force_copy_file(s, d)
        if os.path.isdir(s):
            is_recursive = contains_sub_dir(s)
            if is_recursive:
                copy_files(s, d)
            else:
                force_merge_flat_dir(s, d)


def copy_files(src, dst):
    """
    复制指定目录的文件到另外一个目录
    @param src: 源目录
    @param dst: 目标目录
    @return:
    """
    try:
        _copy_files(src, dst)
    except Exception as e:
        print("ERROR：复制文件失败：" + str(e))
        delete_fd([], src)
        print("请手动解压 python_oa-master.zip 和覆盖资料。")
        exit(-1)


def _unzip(zip_file, root):
    """
    解压缩文件到指定目录
    @param zip_file: 为zip文件的全路径
    @param root: 为解压后的路径
    @return:
    """
    with zipfile.ZipFile(zip_file, "r") as fz:
        for file in fz.namelist():
            fz.extract(file, root)
    fz.close()


def unzip(zip_file, root):
    """
    解压缩文件到指定目录
    @param zip_file: 为zip文件的全路径
    @param root: 为解压后的路径
    @return:
    """
    try:
        _unzip(zip_file, root)
    except Exception as e:
        print("ERROR：解压缩文件失败：" + str(e))
        exit(-1)


def _delete_fd(files, dirs):
    """
    清理临时文件和目录
    @param files:
    @param dirs:
    @return:
    """
    if type(files) is str:
        files = [files]
    if type(dirs) is str:
        dirs = [dirs]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)


def delete_fd(files, dirs):
    """
    清理临时文件和目录
    @param files:
    @param dirs:
    @return:
    """
    try:
        _delete_fd(files, dirs)
    except Exception as e:
        print("ERROR：清理临时文件失败：" + str(e))
        exit(-1)


def _download(url, save_file):
    """
    下载文件
    @param url: 下载地址
    @param save_file: 保存的文件名
    """
    r = requests.get(url)
    with open(save_file, "wb") as code:
        code.write(r.content)


def download(url, save_file):
    """
    下载文件
    @param url: 下载地址
    @param save_file: 保存的文件名
    """
    try:
        _download(url, save_file)
    except Exception as e:
        print("ERROR：下载文件失败：" + str(e))
        exit(-1)


def update_course():
    # now = datetime.datetime.now().strftime('%y%m%d%H')
    # 下载地址
    zip_url = "https://gitcode.net/pythoncr/python_oa/-/archive/master/python_oa-master.zip"
    # 下载保存文件路径
    save_file = "./python_oa-master.zip"
    # 解压缩文件路径
    unzip_dir = "./python_oa-master"
    print("课程资料更新中...")
    # 1、清理临时文件失败
    delete_fd(save_file, unzip_dir)
    # 2、下载文件
    print("课程资料下载中...")
    download(zip_url, save_file)
    # 3、解压文件到当前目录
    print("课程资料解压中...")
    unzip(save_file, "./")
    # 4、复制和覆盖最新的文件到当前目录
    print("课程资料更新中...")
    copy_files(unzip_dir, "./")
    # 5、清理临时文件失败
    delete_fd(save_file, unzip_dir)
    print("课程资料更新完成 ^_^")


if __name__ == '__main__':
    update_course()
