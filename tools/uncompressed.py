def un_xz(xz_file, output_file):
    import lzma
    import shutil
    input_xzfile = 'ffmpeg-6.0.tar.xz'
    output_file = 'ffmpeg-6.0.tar'
    with lzma.open(input_xzfile, 'rb') as input:
        with open(output_file, 'wb') as output:
            shutil.copyfileobj(input, output)


def unzip(zip_file, output_dir=None):
    import zipfile

    with zipfile.ZipFile(zip_file) as z:
        if output_dir is None:
            z.extractall()
        else:
            z.extractall(output_dir)

def un_tar(file_name, output_dir=None):
    import tarfile
    import os
    tar = tarfile.open(file_name)
    if output_dir is None:
        output_dir = file_name.replace(".tar", "")
    names = tar.getnames()
    if os.path.isdir(output_dir):
        pass
    else:
        os.mkdir(output_dir)
        # 由于解压后是许多文件，预先建立同名文件夹
    for name in names:
        tar.extract(name, output_dir)
    tar.close()


if __name__ == '__main__':
    un_tar('ffmpeg-6.0.tar', '.')
