import os


def get_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]



if __name__ == '__main__':
    get_file_name(r'G:\code\SpiderKo\SpiderKo\spider\upanso.py')
