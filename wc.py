#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: wc.py
@time: 2019/5/3 9:40 PM
"""
import os

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

# # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
# d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#
# # Read the whole text.
# text = open(path.join(d, 'words.txt')).read()
#
# # Generate a word cloud image
# wordcloud = WordCloud().generate_from_frequencies(text)
#
# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
#
# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
# The function for processing text with Jieba

# def jieba_processing_txt(text):
#     for word in userdict_list:
#         jieba.add_word(word)
#
#     mywordlist = []
#     seg_list = jieba.cut(text, cut_all=False)
#     liststr = "/ ".join(seg_list)
#
#     with open(stopwords_path, encoding='utf-8') as f_stop:
#         f_stop_text = f_stop.read()
#         f_stop_seg_list = f_stop_text.splitlines()
#
#     for myword in liststr.split('/'):
#         if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
#             mywordlist.append(myword)
#     return ' '.join(mywordlist)

def color_func():
    pass

if __name__ == '__main__':
    dt = {}
    with open('words.txt', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            parts = line.split(' ')
            if len(parts) >= 2:
                dt[parts[0]] = float(parts[len(parts) - 1])
    wc = WordCloud(font_path='/Users/william/Library/Fonts/Alibaba-PuHuiTi-Regular.otf', width=800, height=600,
                   colormap=plt.get_cmap('Set3'))\
        .generate_from_frequencies(dt)
    wc.to_image().show()
    #
    # plt.figure()
    # plt.imshow(img, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

