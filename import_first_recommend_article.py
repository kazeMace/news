import pymysql
from pandas import DataFrame
from pandas import Series
import jieba.analyse
import csv
import django
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
django.setup()
from newsApp.models import Recommend_Article


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='django',charset='utf8')
article = conn.cursor()
article.execute("SELECT * FROM newsapp_article  ORDER BY  RAND() LIMIT 100")
recommend_article_first = conn.cursor()
count=0
for a in article.fetchall():
    print(a)
    article_id = a[0]
    article_name = a[1]
    article_content = a[2]
    date = a[3]
    tag = a[8]
    source = a[9]
    keywords = a[11]
    image1 = a[12]
    image2 = a[13]
    image3 = a[14]
    image4 = a[15]
    image5 = a[16]
    # sql_insert = str("INSERT INTO newsapp_recommend_article(headline,content,date,tag,source,keywords,image1,image2,image3,image4,image5) VALUES ("+str(article_name)+','+str(article_content)+','+str(date)+','+str(tag)+','+str(source)+','+str(keywords)+','+str(image1)+','+str(image2)+','+str(image3)+','+str(image4)+','+str(image5)+")")
    # print(sql_insert)
    # recommend_article_first.execute(sql_insert)
    item = Recommend_Article(
        id = article_id,
        headline=article_name,
        date=date,
        content=article_content,
        tag=tag,
        source=source,
        belong_to_id=1,
        keywords=keywords,
        image1 = image1,
        image2 = image2,
        image3 = image3,
        image4 = image4,
        image5 = image5,
    )
    item.save()


