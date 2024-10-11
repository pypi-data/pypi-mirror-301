import json
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
import os
from PIL import Image
import ddddocr
from tqdm import tqdm



class HuiFontMap:
    def __init__(self,fontpath,savepath,issaveimg=True):
       """
       初始化读取字体和获取字体文件映射
       :param font: 字体文件路径
       :param savepath:字形图片保存路径
       :param issaveimg:是否开启保存图片
       """
       self.font = TTFont(fontpath) # 实例化TTFont
       self.savepath = savepath
       cmap = self.font.getBestCmap()
       if issaveimg:
        self.saveFontImg(cmap=cmap,savepath=savepath)
    def saveFontImg(self,cmap,savepath):
        """
        根据字体文件生成对应字形图像并保存
        :param cmap:字符映射字典
        :param savepath:生成的字形图像保存地址
        :return:无返回值。函数执行后，字形图像将被保存到指定路径。
        """
        for i in tqdm(cmap, desc='任务进行中', unit='items'):
            pen = FreeTypePen(None)  # 实例化Pen子类
            glyph = self.font.getGlyphSet()[cmap[i]] # 通过字形名称选择某一字形对象
            glyph.draw(pen) # “画”出字形轮廓
            width, ascender, descender = glyph.width, self.font['OS/2'].usWinAscent, -self.font['OS/2'].usWinDescent # 获取字形的宽度和上沿以及下沿
            height = ascender - descender # 利用上沿和下沿计算字形高度
            fontimg = pen.image(width=width, height=height, transform=Offset(0, -descender))
            resizeimg = fontimg.resize((200,200), Image.Resampling.LANCZOS)
            old_size = resizeimg.size
            new_size = (400,400)
            red_background = Image.new("RGBA", (400,400), 'red') #红色背景
            red_background.paste(resizeimg, (int((new_size[0] - old_size[0]) / 2),
                                  int((new_size[1] - old_size[1]) / 2)),resizeimg.split()[1])
            red_background.save(os.path.join(savepath ,cmap[i] + '.png'))

        print('字形图片保存完毕')
    def ocrFontImg(self,jsonpath = None):
        """
        :param jsonpath: ocr字典结果的保存路径，默认不保存
        :return: 返回一个ocr识别字典结果
        """
        ocr = ddddocr.DdddOcr()
        file_list = os.listdir(self.savepath)
        dis  = {}
        for i in file_list:
            path = os.path.join(self.savepath,i)
            with open(path, 'rb') as f:
                img_bytes = f.read()
                res = ocr.classification(img_bytes)
                dis[i.split('.')[0]]=res
        print('识别完毕')
        if jsonpath!= None:
            with open(jsonpath, 'w', encoding='utf-8') as f:
                json.dump(dis,fp=f,ensure_ascii=False)
            print('文件已保存')
        return dis

if __name__ == '__main__':
    hui = HuiFontMap(fontpath=r"C:\Users\21761\Desktop\file.woff",savepath=r"C:\Users\21761\Desktop\新建文件夹")
    diststr = hui.ocrFontImg(jsonpath='fontmap.json')
    print(diststr)


