import base64
import hashlib
import hmac

from Crypto import Random
from Crypto.Cipher import AES, DES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from pyDes import des, ECB

"""
pycrypto
pydes

加密算法：DES,AES,RSA, MD5, SHA, HMAC, base64

aes: iv key
des: key
ras: 公钥解密 私钥加密
md5: 不可逆
hmac: 不可逆


https://www.cnblogs.com/sochishun/p/7028056.html

http://91fans.com.cn/post/ilikeaes/#gsc.tab=0


# 加解密测试在线工具
https://blog.zhengxianjun.com/online-tool/crypto/aes/

# https://www.cnblogs.com/xuchunlin/p/11421795.html
python 在 Windows下使用AES时要安装的是pycryptodome 模块   pip install pycryptodome 
python 在 Linux下使用AES时要安装的是pycrypto模块   pip install pycrypto 
"""

__BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size


def pad_byte(b):
    '''
    1 先计算所传入bytes类型文本与16的余数
    2 在将此余数转成bytes 当然用0补位也可以
    3 已知了 余数 那么就用余数*被转成的余数，就得到了需要补全的bytes
    4 拼接原有文本和补位
    :param b: bytes类型的文本
    :return: 返回补全后的bytes文本
    '''
    bytes_num_to_pad = AES.block_size - (len(b) % AES.block_size)
    # python3 中默认unicode转码
    # 实际上byte_to_pad 就已经 将 数字转成了unicode 对应的字符 即使你的入参正好是16的倍数，那么bytes也是把列表整体的转码也是有值的
    # 后边解密的匿名函数 拿到最后一个数字后，就知道应该截取的长度，在反着切片就行了
    # 这样保证了数据的完整性
    byte_to_pad = bytes([bytes_num_to_pad])
    padding = byte_to_pad * bytes_num_to_pad
    print(padding)
    padded = b + padding
    return padded


def base64_encode(bdate):
    """
    已经验证
    b64编码
    Args:
        bdate:

    Returns:

    """
    return base64.b64encode(bdate).decode()


def base64_decode(date_str):
    """
    已经验证
    b64解码
    Args:
        date_str:

    Returns:

    """
    return base64.b64decode(date_str)


def aes_decrypt(key, iv, en_str):
    """
    已经验证
    aes解密
    具体算法：https://www.cnblogs.com/xuchunlin/p/11421795.html
    Args:
        key:
        iv:
        en_str:

    Returns:

    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decryptByts = base64.b64decode(en_str)
    msg = cipher.decrypt(decryptByts).decode()
    paddingLen = ord(msg[len(msg) - 1])
    return msg[0:-paddingLen]


def aes_encrypt(raw_data, key, iv):
    """
    aes加密 已经验证
    Args:
        key:
        iv:
        raw_data:

    Returns:

    """

    # if len(raw_data) < 160:
    #     raw_data = f"{raw_data}"
    #
    # else:
    #     raw_data = f"{raw_data}"

    file_aes = AES.new(key, AES.MODE_CBC, iv)  # 创建AES加密对象
    text = raw_data.encode('utf-8')  # 明文必须编码成字节流数据，即数据类型为bytes
    # 填充值在aes_decrypt可以看到
    while len(text) % 16 != 0:  # 对字节型数据进行长度判断
        text += b''  # 如果字节型数据长度不是16倍整数就进行补充
    en_text = file_aes.encrypt(text)  # 明文进行加密，返回加密后的字节流数据
    return str(base64.b64encode(en_text), encoding='utf-8')  # 将加密后得到的字节流数据进行base64编码并再转换为unicode类型


def rsa_encrypt():
    """
    protected static String dataKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGG6xTS+btRBNzLtdHHvAzSR/PxzGGbLaNSHQMO+mPQo9Lyz43rs8xkuBDxqnl7CKSSiCncBGZgy60S+C31xaIF0ZeeJZZeuZBv6K013eJob/CrCk92DWWy6dsi9N33tB1wJS6S7YhzanWySRDHKb61CNbhEou5BLUd5o+JDHghQIDAQAB";
    protected static String dataKeyRelease = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFv9Ckd3/7VEVLstFvlVstiWsgTYG0S5NpCOWQtQLPdpHjNihHoEibpJdv9l0BxZFg4+MrU8CZjKg2EobdLXYxdcndgigN6qyN6houFN2Try4Kbv5UxgKIsJTU0ZkBLUAjEAfH5fyH3LNEuiT1SMyratE0sEbUMBHF+keQcD9ukwIDAQAB";

    Returns:

    """
    #   this.sendHeader.put("AZTYPKLQJ", "JQLKPYTZA");
    #                 this.sendHeader.put("ONMARCH", "HCRAMNO");
    #                 String r0 = StringUtil.get32UUID();
    #                 this.sendHeader.put("requestid", r0);
    #                 JSONObject jSONObject = new JSONObject();
    #                 jSONObject.put("businessId", "azj");
    #                 jSONObject.put("requestid", r0);
    key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGG6xTS+btRBNzLtdHHvAzSR/PxzGGbLaNSHQMO+mPQo9Lyz43rs8xkuBDxqnl7CKSSiCncBGZgy60S+C31xaIF0ZeeJZZeuZBv6K013eJob/CrCk92DWWy6dsi9N33tB1wJS6S7YhzanWySRDHKb61CNbhEou5BLUd5o+JDHghQIDAQAB\n-----END PUBLIC KEY-----'
    message = '{"AZTYPKLQJ":"JQLKPYTZA","ONMARCH":"HCRAMNO","requestid":"1650901747466","businessId":"azj"}'
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
    print(cipher_text.decode('utf-8'))


def rsa_decrypt():
    """

    Returns:

    """

    en = 'NBvR/QkT2URfd9ZKaF7U++sXLZmd52LxU+THX27ESIE/iWSpGfuaseXo4yUZV1nkb7jV8aTIICxIuMfPOylEHSggnhqMoIm6LUTLBctym4iYvTM89mgCV6N2IlwODk466skxJWuw9PcdQQirZBMcgJ5YMDIsonnz9EEgILk5aUQ='
    random_generator = Random.new().read
    key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGG6xTS+btRBNzLtdHHvAzSR/PxzGGbLaNSHQMO+mPQo9Lyz43rs8xkuBDxqnl7CKSSiCncBGZgy60S+C31xaIF0ZeeJZZeuZBv6K013eJob/CrCk92DWWy6dsi9N33tB1wJS6S7YhzanWySRDHKb61CNbhEou5BLUd5o+JDHghQIDAQAB'
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(en), random_generator)
    print(text.decode('utf-8'))


def des_decrypt(key, text):
    """
    已经验证
    DES 加密
   :param key: 密钥, 长度必须为 16(AES-128)、24(AES-192)、32(AES-256) Bytes 长度
   :param text: 密文
   :return:
   """
    encrypter = DES.new(key.encode(), DES.MODE_ECB)
    length = 8
    count = len(text)
    if count < length:
        add = (length - count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = encrypter.encrypt(text.encode())
    return base64.b64encode(ciphertext).decode()


def des_encrypt(key, text):
    """
    已验证
    des解密
    Args:
        key:
        text:

    Returns:

    """
    des_obj = des(key.encode(), mode=ECB)
    msg = des_obj.decrypt(base64.b64decode(text)).decode('utf-8')
    return msg[0:-5]


def make_md5(raw_str: str, upper=False):
    """
    md5加密
    Args:
        raw_str:
        upper:

    Returns:

    """
    m = hashlib.md5()
    m.update(raw_str.encode())
    if upper:
        return m.hexdigest().upper()
    return m.hexdigest()


def make_hmac(message: str, key: str):
    """
    hmac加密
    :param message:
    :param key:
    :return:
    """
    message = message.encode()
    key = key.encode()
    h = hmac.new(key, message, digestmod='MD5')
    return h.hexdigest()


if __name__ == '__main__':
    """
    注意需要进行 encode  算法接收字节数据并非 str 数据
    """
    # key = 'BE45D593014E4A4EB4449737660876CE'.encode()
    # iv = 'A8909931867B0425'.encode()
    # encrypted = "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";
    # encrypted = encrypted.encode()
    # print(aes_decrypt(key, iv, encrypted))

    key = '7856412346543216'.encode()
    iv = '0392039203920300'.encode()
    # en = 'M0gHEnGj+4SWCAyNgckhNQ=='
    # en ='pAMjUEfX09vaVbts+Y4pow=='
    # en ='azjfussytBO8O6y1WxIq0KMoVhJWdEEQCK+vBdzGXvpEWIJ5OEepT0eeGsjQKQgJTIQQCiCNuLha\ndxMw1J2rz+zXGtsXw6K+VZmTIOU0sjk=\n'
    #     2MGbGXPbFB7m/RBcWvVAFTcQHGXn4BOgcBG6ha3+NjNbf7uKNJquVgMC/Yw3W6UNwtyhaeg6G505Rmf+GFDg0iHpcNPvf6xmG3DXUryszNicbnRpWzLMYopsw33arnJlg09ysBu4rvPjsSbkmJTBayWQ+fVf03+WP2z+2+kKSfQfMk7zDDiPY05OWt+rtOAGS+H6pudbMsY67mnp2Orhkg==
    # en = '2MGbGXPbFB7m/RBcWvVAFTcQHGXn4BOgcBG6ha3+NjNbf7uKNJquVgMC/Yw3W6UNwtyhaeg6G505Rmf+GFDg0iHpcNPvf6xmG3DXUryszNicbnRpWzLMYopsw33arnJlg09ysBu4rvPjsSbkmJTBayWQ+fVf03+WP2z+2+kKSfQfMk7zDDiPY05OWt+rtOAGjYAN/R4VnLypnimOeePLVw=='
    en = 'dPu3JZ3d+R4y9/TG0Pc/ZJadJ75QAaWOrEEew905K0Bo+FKXRtN8SHCAK/OOEuVzpYSWyFWBCGBBXAMUTjap4Mtu226VoTI3tHiUaDG7V+hzndgZvydQ1DCGsnabAfSZfW280ssv+QfC8Jtzrz/X39iYuc1fsg+6HJ1D+LXrdXSe+Im8fGgpu7/eIGeSPNag0OHAKFwsZQo4Z7Bdnc6atmt2sgr6NvNIuGxabsgzdVk='
    print(aes_decrypt(key, iv, en))

    data = '{"spuCode":"SPU2022030515532822","merchantType":2,"productType":"31","leaseType":1,"channelNo":"weChat","merchantCode":"MC202202281706493","productClass":"LC"}'
    # data = '{"currPage":1,"pageSize":10,"word":"租租侠"}'
    print(aes_encrypt(data, key, iv))

    # print(aes_encrypt('1', key, iv))

    # print(des_encrypt('c179010f', 'tZrj85QXFYE='))

    # rsa_decrypt()
    # rsa_encrypt()
