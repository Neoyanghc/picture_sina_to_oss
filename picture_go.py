import os
import re
import requests
import time
import oss2


allFileNum = 0
fileList = []
auth = oss2.Auth('m1cqJj', 'HfFD8keGK8GodUe')  # 详见文档
endpoint = 'http://oss-cn-beijing.aliyuncs.com'  # 地址
bucket = oss2.Bucket(auth, endpoint, 'jackyanghc')  # 项目名称

def findmd(level, path):
    global allFileNum
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            if(f.split('.')[-1] == 'md' or f.split('.')[-1] == 'markdown'):
                fileList.append(path+'/'+f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print( '-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            findmd((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        print('-' * (int(dirList[0])), fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1

def get_pic(src):
    pic=[]
    for pic_url in src:
        r = requests.get(pic_url)
        pic.append(r.content)
    return pic

def search_of_src_of_sina(f):
    pic_name = []
    sina_url = []
    try:
        f_obj = open(f,'r+',encoding="utf-8")
        contents = f_obj.read()
        # 正则匹配寻找 以前sina图床上面的图片
        reg = re.compile('\(https://.*sinaimg.*\)')
        url_s = reg.findall(contents)
        for i in url_s:
            sina_url.append(i[1:-1])
            pic_name.append(i.split('/')[-1])
        pic = get_pic(sina_url)
        oss_url = post_jpg(pic,pic_name)
        for i in range(len(sina_url)):
            contents=contents.replace(sina_url[i],oss_url[i])
        f_obj.seek(0)
        f_obj.write(contents)
        f_obj.close()

    except FileNotFoundError:
        msg = "Sorry, the file " + f + " does not exist."
        print(msg)


#下边的方法是
def post_jpg(pic,jpg_name):
    url = []
    for i in range(len(pic)):
        with open('picture.jpg', 'wb') as file:
            file.write(pic[i])
            file.close()
            result = bucket.put_object_from_file(jpg_name[i], 'picture.jpg')  # 括号内 左边是上传后的文件名，右边是当前系统的文件地址
            print('http status: {0}'.format(result.status))  # 打印上传的返回值 200成功
            jpg_url = bucket.sign_url('GET', jpg_name[i], 60)  # 阿里返回一个关于Zabbix_Graph.jpg的url地址 60是链接60秒有效
            url.append(jpg_url.split('?')[0])
    return url


if __name__ == '__main__':
    PATH='C:/Learning/1'
    findmd(1, PATH)
    print('总文件数 =', allFileNum)

    for f in fileList:
        search_of_src_of_sina(f)
        print("success of",f)




