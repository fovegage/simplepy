import json
import math
import random
import time
from datetime import datetime

from simplepy.resources import phone

phone_data = json.load(phone)


def gen_lng_lat(base_log=102.7, base_lat=25, radius=100000):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    return longitude, latitude


def get_imei():
    # 定义一个长度为14字符类的数字
    num = str(random.randint(10000000000000, 99999999999999))
    # 计算最后一位校验值
    num_list = list(num)
    # 数字和
    math_sum = 0
    for i in range(1, len(num_list) + 1):
        # 如果是偶数
        if i % 2 == 0:
            take_two_num = int(num_list[i - 1]) * 2
            # 判断乘于2之后的数，是一位还是二位，二位的话就，
            # 将个位和十位上的数字相加，一位就保持不变
            if len(str(take_two_num)) == 2:
                for j in list(str(take_two_num)):
                    math_sum = int(j) + math_sum
            else:
                math_sum = take_two_num + math_sum
        # 如果是奇数的话，直接相加
        else:
            math_sum = int(num_list[i - 1]) + math_sum

    # 根据math_sum得出校验位
    last_num = list(str(math_sum))[-1]
    if last_num == 0:
        check_num = 0
        imei = num + str(check_num)
        return imei

    else:
        check_num = 10 - int(last_num)
        imei = num + str(check_num)
        return imei


def gen_mac():
    mac = [
        0x52, 0x54, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac)).upper()


def gen_phone():
    pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    random_pre = random.choice(pre_list)
    number = "".join(random.choice("0123456789") for i in range(8))
    return random_pre + number


def gen_zero_ts():
    start = time.time()
    start_local = time.localtime(start)
    start_format = datetime(year=start_local.tm_year, month=start_local.tm_mon, day=start_local.tm_mday, minute=0,
                            hour=0, microsecond=0)
    start_ts = int(round(start_format.timestamp() * 1000))
    end_format = datetime(year=start_local.tm_year, month=start_local.tm_mon, day=start_local.tm_mday + 1, minute=0,
                          hour=0, microsecond=0)
    end_ts = int(round(end_format.timestamp() * 1000))
    return start_ts, end_ts


def gen_imsi():
    title = "4600"
    second = 0
    while second == 0:
        second = random.randint(1, 8)
    r1 = 10000 + random.randint(1, 90000)
    r2 = 10000 + random.randint(1, 90000)
    new_imsi = title + "" + str(second) + "" + str(r1) + "" + str(r2)
    return new_imsi


def gen_phone_brand():
    brands = list(set([x.get('brand') for x in phone_data]))
    return random.choice(brands)


def gen_phone_model():
    brands = list(set([x.get('title') for x in phone_data]))
    return random.choice(brands)
