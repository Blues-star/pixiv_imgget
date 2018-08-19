from bs4 import BeautifulSoup
import requests
import json
import re

se = requests.session()

Headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    "Connection":
    "keep-alive",
    "Referer":
    ""
}


class Pixiv():
    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.main_url = 'http://www.pixiv.net'
        # 旧版
        self.iflogin = False
        self.headers = {
            'Referer':
            'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        '''
        新版
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            "Connection":"keep-alive",
            "Referer":""
        }
        '''
        self.qhead = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        self.pixiv_id = ''
        self.password = ''
        self.post_key = []
        self.return_to = 'http://www.pixiv.net/'
        self.load_path = 'D:\psdcode\Python\pixiv_pic'
        self.ip_list = []
        self.lastgoal = ""
        self.lastPicID = 0

    def login(self,useremail,password):
        '''
            参数说明:usermail与password都为字符串类型
        '''
        self.pixiv_id = useremail
        self.password = password
        post_key_html = se.get(self.base_url, headers=self.headers).text
        post_key_soup = BeautifulSoup(post_key_html, 'lxml')
        self.post_key = post_key_soup.find('input')['value']
        # 上面是去捕获postkey
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        res = se.post(self.login_url, data=data, headers=self.headers)
        temp = res.text
        self.iflogin = True
        #print(temp)
    def deal(self,img_tag, opt="new"):
            
        '''
            # 将获取到的缩略图网址转化为对应的原图网址
        '''
        if opt == "new":
            pa = "img/"
            ori = img_tag["src"]
            # print(ori)检验通过
            st = ori.find(pa)
            tans = ori[st:len(ori)]
            tans = 'https://i.pximg.net/img-original/' + tans
            # print(tans)
            tans = tans.replace("_master1200.", ".")
            return tans


    def findout(self,the_img_page,picID):
        '''
            0621更新，通过使用bs4逐层取出缩略图地址并返回
            # 根据访问的图片展示网址获取出原图片的部分格式，主要包括日期时间
            # 后期可能不需要此函数
        '''
        par3 = "member_illust.php?mode=manga&amp;illust_id="
        pacID = picID
        p = par3 + str(pacID)
        # e = open("test2.html", "rb")
        ymyhtml = BeautifulSoup(the_img_page, "lxml")
        # ymyhtml.
        myhtml = ymyhtml.find(id="wrapper")
        myhtml = myhtml.find(attrs={'class': 'img-container'})
        myhtml = myhtml.find("a")
        myhtml = myhtml.find("img")
        print(myhtml["src"])
        '''
        <img src="https://i.pximg.net/c/600x600/img-master/img/2018/06/18/12/00/02/69288761_p0_master1200.jpg"
                                            alt="夏のお風呂上り/木なこ@お仕事募集中" title="夏のお風呂上り/木なこ@お仕事募集中" border="0" />
        '''
        return (myhtml)

    def getaddress(self, picID):
        self.lastPicID = picID
        self.headers['Referer'] = self.qhead + str(picID)
        print(self.headers)
        goal = self.qhead + str(picID)
        res = se.get(goal, headers=self.headers)
        with open("test.html", "wb") as e:
            e.write(res.content)
        temp = self.findout(res.text,picID)
        goal = self.deal(temp)
        goal = goal[0:len(goal) - 5]
        self.lastgoal = goal
        print(goal)
        return goal

    def getimg(self,num):
        '''
            num代表图片数量
        '''
        print("开始下载")
        pictype = self.lastgoal[-3:]
        try:
            ans_picture = se.get(self.lastgoal, headers=self.headers)
            print(ans_picture.status_code)
            for i in range(num):
                filename = str(self.lastPicID) + "_p"+str(i)+"." + pictype
                with open(filename, "wb") as e:
                    e.write(ans_picture.content)
                print("获取成功,已保存为" + pictype + "的形式 : " + filename)
        except:
            print("获取失败")

    def download_img(self,pic_ID, ori_add, page_count=1):
        '''
        ori_add :https://i.pximg.net/img-original/img/2018/06/18/12/00/02/69288761_p
        '''
        fstring = ori_add
        ori_filename = str(pic_ID) + "_p"
        filename = ori_filename + "0.png"
        img_date = se.get(fstring + "0.png", headers=self.headers)
        # print(img_date.headers)
        if (int(img_date.headers["Content-Length"]) > 100):
            # print(img_date.text)
            with open(filename, "wb") as o:
                o.write(img_date.content)
                print("成功保存为png格式")
        else:
            filename = ori_filename + "0.jpg"
            img_date = se.get(fstring + "0.jpg", headers=self.headers)
            with open(filename, "wb") as o:
                o.write(img_date.content)
                print("成功保存为jpg格式")


    def getjson(self, picID):
        '''
        初始html文件(res)见test.html,json格式文件的内容(content)见json3.json
        将服务器返回的html文件处理成有关这张图片的json数据格式返回
        '''
        self.lastPicID = picID
        self.headers['Referer'] = self.qhead + str(picID)
        par1 = str(picID) + ":"
        par2 = ",user:"
        # print(self.headers)
        goal = self.qhead + str(picID)
        res = se.get(goal, headers=self.headers)
        with open(str(picID) + ".html", "wb") as e:
            e.write(res.content)
        print("成功获取页面信息")
        content = res.content.decode()
        st = content.find(par1) + len(par1)
        ed = content.find(par2) - 1
        content = content[st:ed]
        date = json.loads(content)
        self.lastgoal = date["urls"]["original"]
        # 记录下当前访问的图片信息
        # print(date["urls"]["original"][-3:])
        return date

    def download(self, picID):
        print("获取到图片ID，已开始执行")
        if self.iflogin == True:
            imagedate = self.getjson(picID)
            # imagedate为json格式，保留大量信息，但下载时只需要其原图地址，在这里仅作为debug信息保留
            self.getimg(num = int(imagedate["pageCount"]))
        else:
            goal = self.getaddress(picID)
            self.download_img(picID,goal)


# onetest()

mypixiv = Pixiv()
mypixiv.login()
while True:
    toimg = int(input("请输入PIXVI图片ID:\n"))
    # mypixiv.login()
    #print(mypixiv.getaddress(69261627))
    # mypixiv.getjson(70217043)
    # mypixiv.getimg()
    mypixiv.download(toimg)
