import os

import cv2

from simplepy.decorators import get_callback_path, get_time
from simplepy.utils import download_image_decode


@get_callback_path
def cal_img(img_filename, **kwargs):
    """
    返回图片的原始宽度和长度
    Args:
        img_filename:
        **kwargs:

    Returns:

    """
    path = kwargs.get('path')
    full_path = os.path.join(path, img_filename)
    img = cv2.imread(full_path)
    sp = img.shape

    height = sp[0]  # height(rows) of image
    width = sp[1]  # width(colums) of image
    rgb = sp[2]  # the pixels value is made up of three primary colors
    return height, width, rgb


@get_time
def get_distance(fg, bg, resize_num=1):
    """
    找出图像中最佳匹配位置
    :param target_src: 目标即背景图
    :param template_src: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    fg_obj = download_image_decode(src=fg)
    fg_gray = cv2.cvtColor(fg_obj, cv2.COLOR_BGR2GRAY)
    bg_obj = download_image_decode(bg, flag=0)

    res = cv2.matchTemplate(fg_gray, bg_obj, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(res)
    distance = max_indx[0] * resize_num
    return distance
