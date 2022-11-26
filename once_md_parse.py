import json
import os
import re
import time
import urllib.parse
import shutil
import requests


def find_all_pic(file_content_: str, md_file_path_: str):
    # 读取文件
    exist_list = []
    not_exist_list = []
    # 通过正则匹配图片标签
    _per_md_pic_list = re.findall(r'!\[.*?]\((.*?)\)', file_content_)
    for _pic in _per_md_pic_list:
        # 如果是url直接跳过
        if _pic.startswith("http"):
            continue
        # pic url '\'转'/' + 反转义
        c_pic = _pic.replace('\\', '/')
        c_pic = urllib.parse.unquote(_pic)
        # 获取图片绝对路径
        pic_absolute_path_ = os.path.join(md_file_path_, c_pic)
        # 判断图片是否存在
        if os.path.exists(pic_absolute_path_):
            exist_list.append({
                "origin_pic_url": _pic,
                "pic_absolute_path": pic_absolute_path_
            })
        else:
            not_exist_list.append(pic_absolute_path_)
    return exist_list, not_exist_list


def replace_pic_in_md(md_text: str, origin_pic_url_: str, new_pic_url_: str):
    # 替换图片
    new_md_text = md_text.replace(origin_pic_url_, new_pic_url_)
    return new_md_text


def upload_pic_module(pic_path: str):
    # 获取文件类型
    file_type = os.path.splitext(pic_path)[1]
    # 获取temp文件夹

    # 时间戳
    timestamp = int(time.time())
    temp_path = os.path.join(os.getcwd(), "temp" + str(timestamp) + file_type)
    #
    # # 复制图片到指定目录
    shutil.copy(pic_path, temp_path)
    # 上传图片
    post_body = {"list": [temp_path]}
    post = requests.post("http://127.0.0.1:36677/upload", data=json.dumps(post_body))
    json_data = json.loads(post.text)
    if json_data['success']:
        # 获取图片url
        os.remove(temp_path)
        _pic_url = json_data['result'][0]
        print("上传成功 %s" % pic_path)
        return _pic_url
    else:
        print("上传失败")
        return None


if __name__ == '__main__':
    from tpl_gui import *

    # 选择文件
    file_path = select_file('D:\\00note\\MD\\Java基础')
    with open(file_path, "r", encoding='utf-8') as md_file:
        file_content = md_file.read()
    el, nel = find_all_pic(file_content_=file_content,
                           md_file_path_=file_path)
    if nel:
        confirm = confirm_gui()
        if not confirm:
            exit()
    print("exist pic list: %s" % el)
    print("not exist pic list: %s" % nel)
    for pic_info in el:
        origin_pic_url = pic_info['origin_pic_url']
        pic_absolute_path = pic_info['pic_absolute_path']
        pic_url = upload_pic_module(pic_path=pic_absolute_path)
        if pic_url:
            file_content = replace_pic_in_md(md_text=file_content, origin_pic_url_=origin_pic_url,
                                             new_pic_url_=pic_url)
    with open(file_path, "w", encoding='utf-8') as md_file:
        md_file.write(file_content)
