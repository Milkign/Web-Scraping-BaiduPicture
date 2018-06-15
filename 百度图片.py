import re
import requests
from requests.exceptions import RequestException


# 引用模块：
# 正则表达式模块：用于匹配
# requests模块：用于数据爬取
# 请求异常模块


# html解析器
def html_baidu(url):
    try:
        # 解析链接
        res = requests.get(url)
        # 若成功访问网页（状态码为200即为成功访问），则运用方法 .text得到文本，否则返回空
        if res.status_code == 200:
            return res.text
        return None
    # 发生请求异常则返回空
    except RequestException:
        return None


# 获取图片
def get_picture(html, keyword, num):
    # objURL 为img图片，编写正则表达式，匹配所有图片，生成列表
    picture = re.findall('"objURL":"(.*?)",', html, re.S)
    # 图片起始数字为1
    i = 1
    print('——已搜索到关键字:' + keyword + '的图片，开始爬取——')

    # pd爬取图片数量，得到相应图片列表
    if num != 0:
        pic_list = picture[:num]
    else:
        pic_list = picture
    print("已获取到图片列表")

    # 循环正则表达式列表，爬取每一张图片
    for item in pic_list:
        print('第' + str(i) + '张图片爬取成功')

        try:
            # 10秒超时控制，防止图片网址打不开
            pic = requests.get(item, timeout=10)
            # 若图片无法爬取，则直接跳过
        except requests.exceptions.ConnectionError:
            continue

        # 为爬取到的图片命名，格式：关键字_序号.jpg,存储路径为本文件上一级目录的img文件夹内
        pic_name = '../img/' + keyword + '_' + str(i) + '.jpg'
        # 存储图片
        keep_picture(pic, pic_name)
        # 更新图片数字
        i += 1


# 存储图片
def keep_picture(picture, name):
    # 存储图片
    f = open(name, 'wb')
    f.write(picture.content)
    f.close()


# 主函数
if __name__ == '__main__':
    kw = input("请输入关键字: ")
    number = input("请输入需要的图片数量(获取全部则输入0): ")
    number = int(number)
    # 提示用户创建img文件夹，确保文件夹存在
    while True:
        print("请于本文件上一级目录创建名为img文件夹，用于存储图片")
        # 确保文件夹存在，不存在则无法保存图片
        n = input("是否已创建img文件夹？（输入y确认）")
        if n == "y":  # 创建文件则进行爬取
            print("准备就绪.....")
            # 生成爬取链接
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + kw + '&ct=201326592&v=flip'
            # 解析链接
            result = html_baidu(url)
            # 图片爬取
            get_picture(result, kw, number)
            print("——图片爬取结束——")
            break
