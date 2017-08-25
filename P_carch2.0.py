import urllib.request
import urllib.error
import re
import json
import threading


def welcome():
    print("欢迎使用非常中二的P站每日排行榜自动下载器，在使用我之前，请先选择一个你想要存放下载文件的文件夹，然后把我放在里面，重新启动本程序")
    print("当前版本为2.0版本，暂时还没有开放下载R18……咳咳那啥的功能，如果有需要，请联系作者“星夜的蓝天”，联系方式：你猜（上B站）。")
    print("所以请米娜桑放心的下载，绝对不会下载到R18的图片或者本子图的（flag在这边立着了，自己去看看镜子找找脸吧）")
    print(
        "好吧实话实说我只能保证下不到本子……要是大家去https://www.pixiv.net/ranking.php?mode=daily这个网址上找到了R18的图片那么我一定可以下到它！！！"
    )
    print("咳咳，冷静点，好呗，开始接入P站P接口")
    print("p站接口接入成功，经过我精准无误的计算（又是一个flag）>>>")


def getHtml(url):
    page = urllib.request.urlopen(url)
    # 获取页面
    temphtml = page.read().decode('utf_8')
    return temphtml


def getjsondate(yuanshuju):
    # reference = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id="
    print("开始读取json表单")
    tempjsondate = json.loads(yuanshuju)
    return tempjsondate


def getdate(num):
    Putindate = {}
    Putindate['format'] = 'json'
    Putindate['mode'] = 'daily'
    Putindate['p'] = str(num)
    # Putindate['tt'] = '2c5c5134a760204aad3cdb0629f7f66c'
    return urllib.parse.urlencode(Putindate).encode('utf-8')


def zhengze(strarry):
    patstr = r'img/\d{4,}/\d{2,}/\d{2,}/\d{2,}/\d{2,}/\d{2,}/\d+_'
    patter = re.compile(patstr)
    result = patter.findall(strarry)
    # print(result[0])
    return (result[0])


def getReferer(url, numID):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p' + str(numID)
    return reference + re.findall(reg, url)[0] + "&page=" + str(numID)


def trytogetimg(filename, number, textnameID):
    # filename示例：https://i.pximg.net/img-original/img/2017/07/24/00/26/01/64019639_p 要加上0.jpg或0.png
    for index in range(int(number)):
        # index表示第几张图
        # 先测试jpg格式，如果request返回404错误代表所get的文件是png
        tempimgadd = filename + str(index) + ".jpg"
        # tempimgadd示例： https://i.pximg.net/img-original/img/2017/07/24/01/00/01/64020381_p0.jpg 完整网址
        Headers['Referer'] = getReferer(tempimgadd, index)
        # 匹配出P站介绍图片的网址，作为请求头提交，用来绕过防盗链
        print("开始尝试获取图片")
        try:
            req = urllib.request.Request(tempimgadd, None, Headers)
            picture = urllib.request.urlopen(req)
            print("获取成功")
            tempfilename = textnameID + "_p" + str(index) + ".jpg"
            with open(tempfilename, "wb") as e:
                e.write(picture.read())
                print("保存成功")
        except urllib.error.HTTPError as myerror:
            print("目标图片非jpg格式，已自动转为png格式获取")
            tempimgadd = filename + str(index) + ".png"
            Headers['Referer'] = getReferer(tempimgadd, index)
            req = urllib.request.Request(tempimgadd, None, Headers)
            picture = urllib.request.urlopen(req)
            print("获取成功")
            tempfilename = textnameID + "_p" + str(index) + ".jpg"
            with open(tempfilename, "wb") as e:
                e.write(picture.read())
                print("保存成功")
    # flag+=1


def onetest():
    '''
    这是一个单图片的测试
    '''
    # "https://i.pximg.net/img-original/img/2017/07/23/12/17/17/64006037_p0.jpg"
    testurl = "https://i.pximg.net/img-original/img/2017/07/24/01/00/01/64020381_p0.png"
    print("开始尝试获取图片")
    Headers['Referer'] = getReferer(testurl, 0)
    req = urllib.request.Request(testurl, None, Headers)
    date = urllib.request.urlopen(req, timeout=10)
    print("获取成功")
    with open("64020381_p0.png", "wb") as e:
        e.write(date.read())
        print("保存成功")


def getpage(n):
    '''
    通过对ranking的请求返回从1到10的请求网址，为字符串数组的形式返回
    '''
    if n >= 1 and n <= 10:
        Anphpurlarr = []
        for i in range(1, n + 1):
            AnswerUrl = "https://www.pixiv.net/ranking.php?mode=daily&p=" + str(
                i) + "&format=json"
            Anphpurlarr.append(AnswerUrl)
            # print(Anphpurlarr)
        return (Anphpurlarr)
    else:
        print("您输入的数据不合法，程序无法启动")
    return (Anphpurlarr)


Headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    "Connection":
    "keep-alive",
    "Referer":
    ""
}
mythreadlist = []
k = 0
flag = 0
welcome()
pagenumber = int(input("请输入你想要的页数，理论上一页50张："))
AnswerUrlArr = getpage(pagenumber)
print("得到今日推荐首页")
HeadUrl = r"https://i.pximg.net/img-original/"
# for i in urlarr:
#    print(i)
# AnswerUrl = "https://www.pixiv.net/ranking.php?mode=daily&p=1&format=json"
for oneurl in AnswerUrlArr:
    # 页面数
    Html = getHtml(oneurl)  # 结果返回正确
    #返回每日推荐榜P站服务器返回的json数组，html格式
    jsondate = getjsondate(Html)
    print("读取json表单完毕")
    # print(jsondate['contents'][0]['url'])
    for innum in jsondate['contents']:
        #用jsondate['contents']来获取今天所有的图片
        print(innum['illust_id'], innum['date'], innum['illust_page_count'])
        # 输出了id，日期（没用），图片数（用if来判断）
        tempaddress = zhengze(innum['url'])
        # 使用正则表达式取出中间部分
        #if innum['illust_page_count'] == "1":
        #如果图片为单图片
        mythreadlist.append(
            threading.Thread(
                target=trytogetimg,
                args=(HeadUrl + tempaddress + "p", innum['illust_page_count'],
                      str(innum['illust_id']))))
        k += 1
        print("已成功填装", k, "个目标")
        '''trytogetimg(HeadUrl + tempaddress + "p", innum['illust_page_count'],
                    str(innum['illust_id']))'''
        # tempimgadd = HeadUrl+tempaddress+"p"+'0.jpg'       测试中的输出语句
        # print(tempimgadd)
print("所有目标填装完毕")
print("请注意，接下来本程序的界面会变得十分乱，是时候可以装一波B了！")
for one in mythreadlist:
    one.start()
'''while True:
    if flag == k :
        print("所有图片已下载完毕")'''
'''
Html = getHtml(AnswerUrl)  #结果返回正确
jsondate = getjsondate(Html)
print("读取json表单完毕")
#print(jsondate['contents'][0]['url'])
for innum in jsondate['contents']:  #用jsondate['contents']来获取今天所有的图片
    print(innum['illust_id'], innum['date'], innum['illust_page_count'])
    # 输出了id，日期（没用），图片数（用if来判断）
    tempaddress = zhengze(innum['url'])
    # 使用正则表达式取出中间部分
    if innum['illust_page_count'] == "1":
        trytogetimg(HeadUrl+tempaddress+"p", innum['illust_page_count'], str(innum['illust_id']))
    # tempimgadd = HeadUrl+tempaddress+"p"+'0.jpg'       测试中的输出语句
    # print(tempimgadd)

print("全部图片获取完毕")
'''
