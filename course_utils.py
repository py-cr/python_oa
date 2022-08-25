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
import hashlib

# 统计更新次数
update_count = 0


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


def get_md5(path):
    d5 = hashlib.md5()  # 生成一个hash的对象
    with open(path, 'rb') as f:
        while True:
            content = f.read(40960)
            if not content:
                break
            d5.update(content)  # 每次读取一部分，然后添加到hash对象里
    # print(‘MD5 : %s‘ % d5.hexdigest())
    return d5.hexdigest()  # 打印16进制的hash值


# 是否为带BOM头的UTF8文件
def is_text_file(pathfile):
    file_extension = str(pathfile).split('.')[-1]
    if file_extension in ['ipynb', 'py', 'md', 'html', 'txt', 'gitignore', 'cmd', 'bat']:
        return True

    return False


def same_text(sfile, dfile):
    try:
        with open(sfile, mode='r', encoding='utf8') as f:
            # 文件读取
            sfile_content = f.read()
        with open(dfile, mode='r', encoding='utf8') as f:
            # 文件读取
            dfile_content = f.read()
        return sfile_content == dfile_content
    except Exception  as e:
        with open(sfile, mode='r') as f:
            # 文件读取
            sfile_content = f.read()
        with open(dfile, mode='r') as f:
            # 文件读取
            dfile_content = f.read()
        return sfile_content == dfile_content
    return False


def samefile(sfile, dfile):
    if os.path.samefile(sfile, dfile):
        return True
    if is_text_file(sfile):
        return same_text(sfile, dfile)
    if get_md5(sfile) == get_md5(dfile):
        return True
    return False


def force_copy_file(sfile, dfile):
    """
    强制复制文件
    @param sfile: 源文件
    @param dfile: 目标文件
    @return:
    """
    global update_count
    if os.path.isfile(sfile):
        if os.path.exists(dfile):
            if samefile(sfile, dfile):
                return
        if not sfile.endswith("更新课程资料.ipynb"):
            update_count += 1
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
    exclude_dirs = [".ipynb_checkpoints", "__pycache__", ".git", ".idea"]
    for d in exclude_dirs:
        if src.endswith(d):
            return

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
                _copy_files(s, d)
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


def zip_dir(dir_path, zipfile_path):
    """
    zip dir
    :param dir_path: where zip dir path
    :param zipfile_path: zip dir
    :return:
    """
    file_list = []
    if os.path.isfile(dir_path):
        file_list.append(dir_path)
    else:
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                file_list.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfile_path, "w", zipfile.zlib.DEFLATED)
    for file_path in file_list:
        _dir = file_path[len(dir_path) - 1:]
        zf.write(file_path, _dir)
    zf.close()


def backup_as_zip(zipfile):
    try:
        zip_dir(".", zipfile)
    except Exception as e:
        print("ERROR：备份文件失败：" + str(e))
        exit(-1)


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


def update_course(backup=True):
    # 下载地址
    zip_url = "https://gitcode.net/pythoncr/python_oa/-/archive/master/python_oa-master.zip"
    # 下载保存文件路径
    save_file = "./python_oa-master.zip"
    # 解压缩文件路径
    unzip_dir = "./python_oa-master"
    print("课程资料开始更新")
    # 1、清理临时文件失败
    delete_fd(save_file, unzip_dir)
    now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    backup_file = f"../python_oa_{now}.zip"
    if backup:
        # 备份当前目录
        backup_as_zip(backup_file)
    # 2、下载文件
    print("下载中...")
    download(zip_url, save_file)
    # 3、解压文件到当前目录
    print("解压中...")
    unzip(save_file, "./")
    # 4、复制和覆盖最新的文件到当前目录
    print("更新中...")
    copy_files(unzip_dir, "./")
    # 5、清理临时文件失败
    delete_fd(save_file, unzip_dir)
    if backup:
        if update_count == 0:
            delete_fd(backup_file, [])
            print("当前的课程资料已经最新 ^_^")
        else:
            print("课程资料更新完成 ^_^")
            print("****** 注意 ******")
            print("课程资料更新会覆盖现有文件，已经进行了备份")
            print("备份路径为：", os.path.abspath(backup_file))
            print("如果更新导致您的文件被覆盖，请手动解压还原。")
            print("******************")


if __name__ == '__main__':
    update_course()
