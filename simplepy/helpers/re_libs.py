import json
import re


def extract_img(text):
    """
    TODO: 获取图片后缀, 提取网页的url

    :param text:
    :return:
    """
    urls = re.findall(r'//(.*?).jpg|.gif｜.jpeg|.png|.JPG|.GIF|.PNG|.JPEG', text, re.I)
    return ['https://' + str(x) + '.jpg' for x in urls if len(x) > 20]


def extract_json_by_re(content):
    """
    提取 jsonp 返回的json内容
    'sm_1642126166228({"code":1100,"message":"success","requestId":"5df76595f659e51faa6be0d950cee01b","riskLevel":"PASS"})'

    Returns:

    """
    return json.loads(re.search('\((.*?)\)', content, re.I).groups()[0])


def delete_html(html):
    """
    去除html标签
    Args:
        html:

    Returns:

    """
    res = re.compile('>(.*?)<')
    text = ''.join(res.findall(html))
    return text


def extract_num(content):
    """
    提取验证码
    :param content:
    :return:
    """
    # content = '321479 is your Instagram code 881'
    rule = re.compile('\d+')
    return rule.findall(content)
