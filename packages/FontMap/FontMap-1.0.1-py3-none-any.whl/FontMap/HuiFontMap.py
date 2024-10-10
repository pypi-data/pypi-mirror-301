# 此代码仅供娱乐---林
import json
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
import os
from PIL import Image
import ddddocr



class HuiFontMap:
    def __init__(self,fontpath,savepath,issaveimg=True):
       """
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
        for i in cmap:
            pen = FreeTypePen(None)  # 实例化Pen子类
            glyph = self.font.getGlyphSet()[cmap[i]] # 通过字形名称选择某一字形对象
            glyph.draw(pen) # “画”出字形轮廓
            width, ascender, descender = glyph.width, self.font['OS/2'].usWinAscent, -self.font['OS/2'].usWinDescent # 获取字形的宽度和上沿以及下沿
            height = ascender - descender # 利用上沿和下沿计算字形高度
            fontimg = pen.image(width=width, height=height, transform=Offset(0, -descender))
            rgba_img = fontimg.convert("RGBA")
            white_background = Image.new("RGBA", (width,height), 'red') #白色背景
            result_img = Image.alpha_composite(white_background, rgba_img)
            result_img.save(os.path.join(savepath ,cmap[i] + '.png'))
        print('字形图片保存完毕')
    def ocrFontImg(self,jsonpath = None):
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
    hui = HuiFontMap(fontpath=r"C:\Users\21761\Desktop\dc027189e0ba4cd.woff2",savepath=r"C:\Users\21761\Desktop\新建文件夹")
    diststr = hui.ocrFontImg(jsonpath='fontmap.json')
    print(diststr)

