# coding=utf-8
from lxml import etree
import requests


class ImagePic(object):
    def __init__(self):
        # http://tieba.baidu.com/f?kw=%E7%BE%8E%E9%A3%9F&ie=utf-8&pn=50
        self.base_url = "http://tieba.baidu.com/f?"
        self.User_agent ={'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}

    def load_page(self, url, data=''):
        html = requests.get(url=url, params=data, headers=self.User_agent).content
        return html

    def load_xml(self,html):
        title_xml = etree.HTML(html)
        link_list = title_xml.xpath("//div[@class='t_con cleafix']/div/div/div/a/@href")
        for link in link_list:
            url = "http://tieba.baidu.com"
            print '==请求帖子=='
            detail_html = self.load_page(url=url+link)
            self.load_image(detail_html)

    def load_image(self, html):
        html = etree.HTML(html)
        link_list = html.xpath("//img[@class='BDE_Image']/@src")
        print link_list
        for link in link_list:
            img_data = self.load_page(url=link)
            self.save_img(img_data, link[-10:])

    def save_img(self,data, filename):
        print type(data)
        with open('./image'+filename, "wb") as f:
            f.write(data)

    def start(self):
        name = raw_input('请输入贴吧名称：')
        page_num = int(raw_input('请输入页码：'))
        pn = (page_num-1)*50
        data = {'kw':name,
                'pn':pn,
                'ie' : 'utf - 8'
                }
        title_html = self.load_page(url=self.base_url, data=data)
        self.load_xml(title_html)

if __name__ == '__main__':
    tieba = ImagePic()
    tieba.start()