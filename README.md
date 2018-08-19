# pixiv爬虫
## 2.5版本，一个P站的小爬虫项目

经过一个版本的更新，已经实现无需登录，但是如果登录后，会有更好的体验
使用方法如下
```python
youpix = Pixiv()
youpix.login("yourmail","yourpwd")
picID = "你想要的图片的ID"
youpix.download(picID)
```
> 由于没有加入防超时机制，所以有可能会长时间不动，请稍等或直接关闭本程序
> 多次下载的话只需要手动添加while循环即可