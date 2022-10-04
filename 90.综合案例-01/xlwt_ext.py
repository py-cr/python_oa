# -*- coding: utf-8 -*-
# @Time    : 2022/4/23 15:30
# @Author  : Python超人
# @FileName: xlwt_ext.py

# xlwt 工具包可以对 xls 文件进行写操作
# xlwt 的命名是 excel writer 简写，很容易记忆
import os
import xlrd
import xlwt
# 自定义工具包
from mail import Mail
from xlwt_styles import create_style


def create_salary_attachment(staff_name, field_names, staff_data):
    """
    创建工资明细单附件（参考课程：90.综合案例-01/01.Excel工资单生成_02）
    :param staff_name: 员工姓名
    :param field_names: 薪资字段
    :param staff_data: 当前员工的薪资数据明细
    :return: 返回工资单附件的路径
    """
    # 看看要生成的表格样式，共有4个
    # 合并单元格的样式（背景=草绿，文字颜色=白色，字号=12，水平对齐=居中）
    merge_style = create_style(back_color=57, font_color=1, font_size=12, horz=2)  # 标题显示用黄色背景图案
    # 字段样式（背景=草绿，文字颜色=白色，字号=12，水平对齐=靠右）
    field_style = create_style(back_color=57, font_color=1, font_size=12, horz=3)
    # 数据值的样式（背景=白色，文字颜色=黑色，字号=12，水平对齐=居中）
    value_style = create_style(back_color=1, font_color=0, font_size=12, horz=2)
    # 金额值的样式（背景=白色，文字颜色=黑色，字号=12，水平对齐=靠右，人民币格式）
    rmb_style = create_style(back_color=1, font_color=0, font_size=12, horz=3, num_format_str="￥#,##0.00;￥-#,##0.00")
    # *******************************************************************
    # 创建写入工作簿对象（放到循环内了，因为一个循环需要新建一个Excel文件）
    # *******************************************************************
    workbook_wt = xlwt.Workbook(encoding='utf-8')

    # 创建工作表，工作表名就是员工姓名
    sheet_wt_staff = workbook_wt.add_sheet(staff_name)

    # 第二循环：遍历字段和数据
    for field_index, field_name in enumerate(field_names):
        row = field_index + 1  # field_index 从 0 开始，则 row 从 1 开始

        if field_index < 14:  # “实发”是最后一个字段名（索引=14），不写入，后面合并单元格再写入
            # 第3列（c=2）写入字段名
            sheet_wt_staff.write(r=row, c=2, label=field_name, style=field_style)
        # else: 如果没有逻辑，可以省略。只对于“实发”字段名不写入了，后面合并单元格再写入

        value = staff_data[field_index]

        if field_index <= 2:  # 0，1，2 三个字段分别是月份、部门、姓名
            sheet_wt_staff.write(r=row, c=3, label=value, style=value_style)  # 第4列（c=3）写入数据
        else:  # 3、4、5...都是金额字段，用RMB货币样式
            sheet_wt_staff.write(r=row, c=3, label=value, style=rmb_style)  # 第4列（c=3）写入数据

    # 设置字段列和数据列的列宽 256 × 宽度默认单位（字符）
    sheet_wt_staff.col(1).width = 256 * 12
    sheet_wt_staff.col(2).width = 256 * 15
    sheet_wt_staff.col(3).width = 256 * 20
    # 合并单元格写入
    sheet_wt_staff.write_merge(r1=1, r2=8, c1=1, c2=1, label="收\n入", style=merge_style)
    sheet_wt_staff.write_merge(r1=9, r2=14, c1=1, c2=1, label="扣\n款", style=merge_style)
    sheet_wt_staff.write_merge(r1=15, r2=15, c1=1, c2=2, label="实发", style=field_style)
    # *******************************************************************
    # 一个循环需要新建一个Excel文件，文件名变化的部分就是员工姓名
    xls_filename_wt = "./files/%s的工资单明细.xls" % staff_name
    workbook_wt.save(xls_filename_wt)  # 保存 Excel
    print("文件 %s 生成成功" % xls_filename_wt)
    return xls_filename_wt
    # *******************************************************************


def get_salary_data(xls_filename):
    """
    获取指定文件的工资单数据
    :param xls_filename: Excel 文件名路径
    :return: 员工姓名列表、字段名称列表、薪资数据列表、电子邮箱列表
    """
    # 读取 Excel（xls_filename_rd 变量刚才已经定义），得到工作簿，赋值给变量 workbook_rd
    workbook_rd = xlrd.open_workbook(xls_filename)

    # 获取第一个工作表，赋值给变量 sheet_rd
    sheet_rd = workbook_rd.sheet_by_index(0)

    # 获取工作表中表格的所有字段（第一行是字段名），记住后面会用到
    field_names = sheet_rd.row_values(0)
    field_names = field_names[0:-1]  # 最后一个是电子邮件（排除掉）
    # print("字段名：",field_names)  # 打印一下看看字段名

    # 创建两个“空”列表变量
    staff_names = []  # 员工姓名列表
    emails = []
    staff_values_list = []  # 员工数据明细列表（这个就是列表中的列表）

    # 因为第一行（索引=0）是字段名，所以从第二行（索引=1）开始读数据
    for row_index in range(1, sheet_rd.nrows):
        values = sheet_rd.row_values(row_index)  # 获取员工的数据列表
        staff_name = values[2]  # 第三列是姓名
        email = values[-1]  # 最后一个是电子邮箱
        staff_names.append(staff_name)  # 追加员工姓名
        emails.append(email)  # 追加员工的电子邮箱
        values = values[0:-1]  # 最后一个是电子邮件（排除掉）
        staff_values_list.append(values)  # 列表中可以再包含列表 [[...],[...]]

    # 员工姓名列表、字段名称列表、薪资数据列表、电子邮箱列表
    return staff_names, field_names, staff_values_list, emails
