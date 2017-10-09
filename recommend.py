import pymysql
from pandas import DataFrame
from pandas import Series
import jieba.analyse
import csv
import django
import datetime
import os
import codecs
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
django.setup()

from newsApp.models import Recommend_Article
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='django',charset='utf8')
user_curs = conn.cursor()
user_curs.execute("SELECT auth_user.id, auth_user.username FROM auth_user WHERE auth_user.is_superuser IS FALSE")

for user in user_curs.fetchall():
    user_id = user[0]
    username = user[1].strip()
    print("user_id:")
    print(user_id)

    get_date_time = conn.cursor()
    get_date_time.execute(
        "SELECT DISTINCT newsapp_userlog.date FROM newsapp_userlog WHERE newsapp_userlog.belong_to_id={} ORDER BY newsapp_userlog.date DESC LIMIT 1".format(str(user_id)))

    # print(get_date_time)
    for date_time in get_date_time.fetchall():
        date = date_time[0].strftime("%Y-%m-%d")
        path = str('D:/recommend_article_id_' + str(user_id) + '.data')
        with open(path, 'r', encoding='utf-8') as f:
            article_id_list = []
            for i in f:
                print(i)
                article_id_list += i.strip().replace('[','').strip().replace(']','').strip().split(',')
            print(type(article_id_list))
            for article_id in article_id_list:
                print(article_id)
                print(type(article_id))
                clean_article_id = article_id.replace("'",'').strip()
                print(clean_article_id)
                article_curs = conn.cursor()
                sql = "SELECT * FROM newsapp_article WHERE newsapp_article.id={}".format(str(article_id))
                print(sql)
                article_curs.execute(sql)
                for i in article_curs.fetchall():
                    id = i[0]
                    headline = i[1].strip()
                    content = i[2].strip()
                    date = i[3]
                    views = i[4]
                    like = i[5]
                    dislike = i[6]
                    recommend = i[7]
                    tag = i[8].strip()
                    source = i[9].strip()
                    url = i[10].strip()
                    print(url)
                    keywords = i[11]
                    image1 = i[12].strip()
                    image2 = i[13].strip()
                    image3 = i[14].strip()
                    image4 = i[15].strip()
                    image5 = i[16].strip()
                    check = Recommend_Article.objects.filter(article_id=id, belong_to_id=user_id)
                    if check:
                        pass
                    else:

                        item = Recommend_Article(
                            article_id=id,
                            headline=headline,
                            content=content,
                            date=date,

                            recommend=1,
                            tag=tag,
                            source=source,

                            keywords=keywords,
                            image1=image1,
                            image2=image2,
                            image3=image3,
                            image4=image4,
                            image5=image5,
                            belong_to_id=user_id,
                        )
                    try:
                        item.save()
                    except:
                        pass

