from SpiderKo.core.db import ClientDb

redis_client = ClientDb.redis_client()


class Bit:
    def __init__(self, site):
        self.site = site

    def bitmap(self):
        st = redis_client.get(self.site)
        obj = bytearray(st)
        return (len(obj) - 1) * 8 + self._get_height_bit(bin(obj[-1]))

    def set_bit(self, index):
        redis_client.setbit(self.site, index, 1)

    @staticmethod
    def _get_height_bit(st):
        new_st = st.lstrip('0b')
        new_len = len(new_st)
        if new_len != 8:
            new_st = (8 - new_len) * '0' + new_st
        return new_st.rfind('1')


if __name__ == '__main__':
    bit = Bit('upanso')
    start = bit.bitmap()
    print(start)
