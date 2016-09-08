#!/home/jamin/anaconda2/bin/python python
# -*-coding:utf-8 -*-
import searchengine
from os import path
import searchengine
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import datetime, calendar,os

def generateDB():
    crawler=searchengine.crawler('searchindex.db')
    crawler.createindextables()
    pages=['http://www.chinagrain.cn/']
    try:
        crawler.crawl(pages,maxpages=100)
    except Exception,e:
        print Exception,":",e
    finally:
        crawler.calculatepagerank()
def generatePosNegFile(filepath):
    f=open(filepath,'w')
    e=searchengine.searcher('searchindex.db')
    cursor= e.con.execute(
            " select * from urllist where posnegscore is not null order by posnegscore desc limit 3  " )
    for row in cursor:
        f.write(row[0])
        f.write("\t")
        f.write(str(row[1]))
        f.write("\t")
        f.write("pos")
        f.write("\n")
    cursor= e.con.execute(
            " select * from urllist where posnegscore is not null order by posnegscore asc limit 3  " )
    for row in cursor:
        f.write(row[0])
        f.write("\t")
        f.write(str(row[1]))
        f.write("\t")
        f.write("neg")
        f.write("\n")
    f.close()
def generateFig(filePath):
    e=searchengine.searcher('searchindex.db')
    frequencies= e.getFrequentWords()
    # take relative word frequencies into account, lower max_font_size
    #wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
    wordcloud = WordCloud(font_path='/home/jamin/Documents/resource/msyh.ttf',background_color="white",stopwords=STOPWORDS.add(u"黄豆"),max_font_size=40, relative_scaling=.25).fit_words(frequencies)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(filePath)
if __name__=='__main__':
    date=datetime.date.today()
    filepath="data/"+str(date)+"pos_neg.txt"
    generatePosNegFile(filepath)
    imgpath="data/"+str(date)+"word_cloud.jpg"
    generateFig(imgpath)
