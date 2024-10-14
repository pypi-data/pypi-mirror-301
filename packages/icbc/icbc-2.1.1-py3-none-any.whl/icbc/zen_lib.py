# coding:utf-8
"""
corp for esp32 未测试

"""
import os
import time
def argv():
    import sys
    return sys.argv
def params():
    import sys
    return sys.argv
def exec_code (code, area=globals()):
    """run python code
    todo"""
    if isinstance(code, str):
        exec(code, area)
          
# 数据读取功能
def load_data(filename, sep=None):
    "读取文件，并每行按tab分列，然后返回list"
    f = open(filename, "r")
    tmp = []
    if sep == None:
        for i in f:
            tmp.append(i)
    else:
        for i in f:
            tmp.append(i.split("\t"))
    f.close()
    return tmp
def load_txt(filename):
    "读取文本文件"
    content = False
    if os.path.exists(filename) and os.path.isfile(filename):
        f = open(filename, "r")
        try:
             content = f.read()
        finally:
             f.close()
    return content
def write_txt(filename, content, encoding=None,mode="w"):
    "写入文本文件"
    f = open(filename, mode,encoding=encoding)
    f.write(content)
    f.close()
def replace(content, replace_dict):
    "对字符串进行批量替换"
    for i in replace_dict:
        if content.count(i):
            content.replace(i, replace_dict[i])
    return content
# 时间、格式功能
def fmt(time_current=None, time_format="%Y%m%d_%H%M%S"):
    "时间字符串生成: 20150819_102959"
    if time_current == None:
        time_current = time.time()
    return time.strftime (time_format, time.localtime(time_current))
def fmt_time(time_current=None, time_format="%Y/%m/%d %H:%M:%S"):
    "标准时间字符串生成: 2015/08/19 10:29:59"
    return fmt(time_current,time_format)
def fmt_mili(time_format="%Y%m%d_%H%M%S_"):
    "生成时间字符串,格式:20161230_101111_321"
    time_current = time.time()
    return fmt(time_current, time_format) + str(time_current % 10)[2:5]
def fmt_decode(time_string, time_format="%Y%m%d_%H:%M:%S"):
    "时间字符串解码,默认格式:%Y%m%d_%H:%M:%S"
    return time.mktime(time.strptime (time_string, time_format))
def fmt_delta(time_string1, time_string2, time_format="%Y%m%d_%H%M%S"):
    "时间字符串计算时间差，默认格式%Y%m%d_%H%M%S"
    return time.mktime(time.strptime (time_string2, time_format)) - time.mktime(time.strptime (time_string1, time_format))
def fmt_convert(time_string, format_from, format_to):
    "时间字符串计算时间差，默认格式%Y%m%d_%H%M%S"
    return time.strftime(format_to, time.strptime (time_string, format_from))
def date(time_current=None):
    return fmt(time_current, "%Y%m%d")
def second():
    return int(time.time())
def sleep(t=0.1):
    "等待x秒"
    time.sleep(t)
    
# 单独功能
def random(end=100, start=0):
    "产生随机数"
    import random
    return random.randint(start, end)

def md5(string,encoding="utf-8"):
    """calculate md5 for string
    计算字符串md5"""
    from hashlib import md5
    m = md5()
    if type(string)==str:
        m.update(string.encode(encoding))
    else:
        m.update(string)
    return m.hexdigest()
def secret_calc(secret="str",encoding="utf-8"):
    sec_int = 0
    for i in base64_encode(secret,1,encoding):
        sec_int = sec_int + ord(i)
    return sec_int
    
def encode(str_source, secret_key="",encoding="utf-8"):
    tmp = base64_encode(str_source,encoding=encoding)
    secret_int = secret_calc(secret_key) % len(tmp)
    return tmp[secret_int:] + tmp[0:secret_int]
def decode(str_source, secret_key="",encoding="utf-8"):
    secret_int = len(str_source) -secret_calc(secret_key) % len(str_source)
    str_source = str_source[secret_int:] + str_source[0:secret_int]
    try:
        return base64_decode(str_source,encoding=encoding)
    except:
        return None

# 文件、筛选目录功能
def list_file(folder=os.getcwd(), filetype=None, is_fullpath=False):
    """获取文件列表，可添加格式list筛选"""
    tmp = os.listdir(folder)
    if is_fullpath:
        result = [os.path.join(folder, i) for i in tmp if os.path.isfile(os.path.join(folder, i))]
    else:
        result = [i for i in tmp if os.path.isfile(os.path.join(folder, i))]
    if not filetype == None:
        "过滤文件类型"
        result = filter_filetype(filetype, result)
    return result

def list_file_all(folder=os.getcwd(), filetype=None, is_fullpath=False):
    """列举所有文件"""
    result = []
    if is_fullpath:
        for root, dirs, files in os.walk(folder):
            for ff in files:
                result.append(os.path.join(root, ff))
    else:
        for root, dirs, files in os.walk(folder):
            for ff in files:
                result.append(ff)
    if not filetype == None:
        """过滤文件类型"""
        result = filter_filetype(filetype, result)
    return result
def list_folder(folder=os.getcwd(),is_fullpath=False):
    """获取文件列表，可添加格式list筛选"""
    tmp = os.listdir(folder)
    result = []
    for i in tmp:
        if os.path.isdir(os.path.join(folder, i)):
            if is_fullpath:
                result.append(os.path.abspath(i))
            else:
                result.append(i)
    return result
def list_folder_all(folder=os.getcwd()):
    """获取文件夹下全部文件夹"""
    result = []
    for i in os.walk(folder):
        if os.path.isdir(i[0]):
            result.append(i[0] + os.sep)
    return result
def filter_filetype(file_type, data):
    """
    对list过滤文件类型
    flist=filter_filetype(["txt"],filelist)
    """
    
    if isinstance(file_type, str):
        file_types = ["." + file_type]
    elif isinstance(file_type, list):
        file_types = ["." + i for i in file_type if isinstance(i, str)]
    else:
        file_types = []
    return [i for i in data if file_ext(i) in file_types]
def file_ext(filename):
    "取得拓展名"
#         dot_pos = filename.rfind(".")
#         return filename[dot_pos:] if 0 < dot_pos < (len(filename) - 1) > 1 else ""todo 测试哪种更快
    return os.path.splitext(filename)[1]
def file_name(filename):
    "去除拓展名"
    return os.path.splitext(filename)[0]
def join(*p):
    """os.path.join()todo test and fix"""
    return os.path.join(*p)
def getcwd():
    """取得当前工作路径todo test and fix"""
    return os.getcwd()
def dirname(p):
    return os.path.dirname(p)
def copy(old, new):
    """复制文件todo test and fix"""
    import shutil
    shutil.copy(old, new)
def move(old, new):
    """移动文件todo test and fix"""
    os.rename(old, new)
def rename(old, new):
    """重命名文件todo test and fix"""
    os.rename(old, new)
def delete(filename):
    """删除文件todo test and fix"""
    os.remove(filename)
def remove(filename):
    """删除文件todo test and fix"""
    os.remove(filename)
def chdir(path=os.getcwd()):
    """修改当前路径"""
    os.chdir(path)
def chmod(file, mode=0o777):
    """修改指定文件权限，默认权限0o777"""
    os.chmod(file, mode)
def abspath(filename=""):
    """获取绝对路径"""
    return os.path.abspath(filename)
def exists(filename):
    """判断文件是否存在"""
    return os.path.exists(filename)
def isdir(filename):
    """判断是否目录"""
    return os.path.isdir(filename)
def folder(path=""):
    """判断是否路径是否存在目录，否则自动新建该目录"""
    path = abspath(path)
    if not os.path.exists (path):
        path_parent = os.path.split(path)[0]
        if not path == path_parent:
            folder(path_parent)
        os.mkdir(path)
    return path
def get_ip():
    """取得本机ip"""
    import socket
    hostname = socket.gethostname()  
    ip = socket.gethostbyname(hostname)
    return ip
def get_hostname():
    """取得本机hostname"""
    import socket
    hostname = socket.gethostname()  
    return ip

# 存储、读取功能
def save(obj, filename=None):
    "序列化保存"
    import pickle
    if filename == None:
        return pickle.dumps(obj)
    else:
        f = open(filename, "wb")
        pickle.dump(obj, f, -1)
        f.close()
def loads(dump_string):
    "序列化读取"
    import pickle
    return pickle.loads(dump_string)
def load(filename,error_default=None):
    "序列化读取本地文件"
    import pickle
    try:
        if exists(filename):
            f = open(filename, "rb")
            result = pickle.load(f)
            f.close()
        else:
            result = error_default
            dbp (filename, "不存在，返回默认/空对象")
    except:
        import traceback
        traceback.print_exc()
        result = error_default
        dbp (filename, "该文件无法读取或者有错误，返回默认/空对象")
        
    return result
def json_loads(json_string):
    import json
    return json.loads(json_string)
def json_dumps(data):
    import json
    return json.dumps(data)


def kv_get(key):
    """key-value get 使用前kv_init"""
    global kvdict
    if kvdict == None:
        dbp ("kv_dict not init")
        return None
    if key in kvdict:
        return kvdict[key]
    else:
        return None
def kv_put(key, value):
    """key-value put 使用前kv_init"""
    global kvdict, kvdict_filename
    if kvdict == None:
        dbp("kv_dict not init")
        return None
    kvdict[key] = value
    save(kvdict, kvdict_filename)
def kv_init(filename):
    """key-value init"""
    global kvdict_filename, kv_dict
    kvdict_filename = filename
    kvdict = load(filename)
def main_menu(ddd):
    print ("please select funcion to run:")
    for i in range (len(ddd)):
        print (i, ddd[i].__name__, ddd[i])
    choice = int(input("choice:"))
    ddd[choice]()
def ramfile(filename=None):
    from io import StringIO
    class ramfile(StringIO):
        def open(self, filename, mode):
            f = open(filename, mode)
            try:
                self.write(f.read())
            finally:
                f.close()
            self.io.seek(0)
        def save(self, filename, mode):
            self.seek(0)
            f = open(filename, mode)
            try:
                f.write(self.read())
            finally:
                f.close()
    if filename:
        f = open(filename, "rb")
        try:
             tmpIO.write(f.read())
        finally:
             f.close()
    return tmpIO
if __name__ == "__main__":
    dd = []
    main_menu(dd)
