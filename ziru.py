import requests  # 导入 requests 库，用于发送 HTTP 请求
from lxml import etree  # 导入 lxml 库中的 etree 模块，用于解析 HTML/XML
from urllib import request  # 导入 urllib 库中的 request 模块，用于发送 HTTP 请求
from PIL import Image  # 导入 PIL 库中的 Image 模块，用于打开和处理图像
import re  # 导入 re 模块，用于正则表达式操作
import pytesseract  # 导入 pytesseract 库，用于识别图像中的文本

class ZiRoom(object):
    # 获取网页源码和图片
    def get_html_img(self):
        # 目标 url
        url = 'https://www.ziroom.com/z/p50-q888769217579814913/'
        # 请求头
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        # 发送 GET 请求
        res = requests.get(url, headers=head)
        # 获取响应的 HTML 内容
        html = res.text
        # 打印响应内容
        # print(html)
        # 匹配图片 url
        img_url = 'https:' + re.search(r'url\((.*?)\);', html, re.S).group(1)
        # 打印图片 url
        # print(img_url)
        # 下载图片并保存到本地
        request.urlretrieve(img_url, '数字.jpg')
        # 返回 HTML 内容
        return html

    # 解析数据
    def parse_data(self, html, replace_dict):
        # 解析 HTML 内容
        tree = etree.HTML(html)
        # 获取房屋数据
        div_list = tree.xpath('//div[@class="Z_list-box"]/div[@class="item"]')
        for div in div_list:
            try:
                # 获取标题文本
                title = div.xpath('.//h5[contains(@class, "title ")]/a/text()')
                # 打印标题
                print(title)
                # 获取价格元素列表
                span_lst = div.xpath('.//div[@class="price "]/span[@class="num"]')
                # 价格
                price = ''
                for span in span_lst:
                    # 获取偏移量
                    # 获取价格元素的 style 属性值
                    style = span.xpath('./@style')[0]
                    # 提取 style 属性值中的位置信息
                    position = style.split(': ')[-1]
                    # 根据位置信息在替换字典中找到对应的数字
                    num = replace_dict[position]
                    # 拼接数字
                    price = price + num
                # 获取价格单位
                end = div.xpath('.//span[@class="unit"]/text()')[0]
                # 拼接价格
                price = price + end
                # 打印价格
                print(price)
            except:
                pass

    # 处理主逻辑
    def main(self):
        # 获取 HTML 内容并下载图片
        html = self.get_html_img()
        # 打开图片文件，并创建一个 Image 对象
        img = Image.open('数字.jpg')
        # 使用 pytesseract 库对图像进行文本识别
        img_res = pytesseract.image_to_string(img)
        # 打印图像识别
        # print(img_res)
        # 使用正则表达式提取图像识别结果中的数字，数字转变成列表
        num_lst = re.findall('\d', img_res)
        # 打印提取的数字列表
        # print(num_lst)
        # 偏移量列表
        x_lst = ['-0px', '-21.4px', '-42.8px', '-64.2px', '-85.6px', '-107px', '-128.4px', '-149.8px', '-171.2px','-192.6px']
        # 两个列表合并成一个字典
        replace_dict = dict(zip(x_lst, num_lst))
        # 解析数据
        self.parse_data(html, replace_dict)

# 创建 ZiRoom 对象
zr = ZiRoom()
# 调用主函数开始执行代码
zr.main()