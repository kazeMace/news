import csv
import pymongo
import django
import datetime
import os
import pymysql
from pandas import DataFrame
from pandas import Series
'''
 auth_user.id,auth_user.username,newsapp_userprofile.nickname,newsapp_userprofile.birth,newsapp_userprofile.sex,newsapp_userprofile.location,newsapp_userprofile.school,newsapp_userprofile.vocation,newsapp_userprofile.china,newsapp_userprofile.world,newsapp_userprofile.social,newsapp_userprofile.mil,newsapp_userprofile.sport,newsapp_userprofile.tech,newsapp_userprofile.economic,newsapp_userprofile.funny,newsapp_ticket.choice,newsapp_article.id,newsapp_article.headline,newsapp_article.url,newsapp_article.tag,newsapp_article.keywords,newsapp_userlog.last_time,newsapp_userlog.times,newsapp_userlog.like_keywords
'''
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='django',charset='utf8')
cur1 = conn.cursor()
cur1.execute("SELECT * FROM newsapp_article")
cur2 = conn.cursor()
# cur2.execute("SELECT * FROM auth_user,newsapp_userprofile,newsapp_ticket,newsapp_userlog WHERE auth_user.id=newsApp_userprofile.belong_to_id AND newsApp_ticket.voter_id=auth_user.id")
cur2.execute("SELECT  auth_user.id,auth_user.username,newsapp_userprofile.nickname,newsapp_userprofile.birth,newsapp_userprofile.sex,newsapp_userprofile.location,newsapp_userprofile.school,newsapp_userprofile.vocation,newsapp_userprofile.china,newsapp_userprofile.world,newsapp_userprofile.social,newsapp_userprofile.mil,newsapp_userprofile.sport,newsapp_userprofile.tech,newsapp_userprofile.economic,newsapp_userprofile.funny,newsapp_ticket.choice,newsapp_article.id,newsapp_article.headline,newsapp_article.url,newsapp_article.tag,newsapp_article.keywords,newsapp_userlog.last_time,newsapp_userlog.times,newsapp_userlog.like_keywords FROM auth_user,newsapp_userprofile,newsapp_ticket,newsapp_userlog,newsapp_article WHERE auth_user.id=newsApp_userprofile.belong_to_id AND newsApp_ticket.voter_id=auth_user.id AND newsApp_ticket.article_id=newsapp_article.id AND newsapp_userlog.belong_to_id=auth_user.id AND newsapp_userlog.article_id=newsapp_article.id")

# cur3 = conn.cursor()
# cur3.execute("SELECT  auth_user.id,auth_user.username,newsapp_userprofile.nickname,newsapp_userprofile.birth,newsapp_userprofile.sex,newsapp_userprofile.location,newsapp_userprofile.school,newsapp_userprofile.vocation,newsapp_userprofile.china,newsapp_userprofile.world,newsapp_userprofile.social,newsapp_userprofile.mil,newsapp_userprofile.sport,newsapp_userprofile.tech,newsapp_userprofile.economic,newsapp_userprofile.funny,newsapp_ticket.choice,newsapp_article.id,newsapp_article.headline,newsapp_article.url,newsapp_article.tag,newsapp_article.keywords,newsapp_userlog.last_time,newsapp_userlog.times,newsapp_userlog.like_keywords FROM auth_user,newsapp_userprofile,newsapp_ticket,newsapp_userlog,newsapp_article WHERE auth_user.id=newsApp_userprofile.belong_to_id AND newsApp_ticket.voter_id=auth_user.id AND newsApp_ticket.article_id=newsapp_article.id AND newsapp_userlog.belong_to_id=auth_user.id AND newsapp_userlog.article_id=newsapp_article.id")

'''
FULL OUTER JOIN newsapp_ticket ON newsApp_ticket.voter_id=auth_user.id FULL OUTER JOIN newsapp_userlog ON newsapp_userlog.belong_to_id=auth_user.id FULL OUTER JOIN  newsapp_article ON newsApp_ticket.article_id=newsapp_article.id AND newsapp_userlog.article_id=newsapp_article.id WHERE auth_user.is_superuser is FALSE
'''

'''

,newsapp_ticket.choice,newsapp_article.id,newsapp_article.headline,newsapp_article.url,newsapp_article.tag,newsapp_article.keywords,newsapp_userlog.last_time,newsapp_userlog.times,newsapp_userlog.like_keywords



JOIN newsapp_article ON newsapp_article.id=newsapp_ticket.article_id AND newsapp_article.id = newsapp_userlog.article_id 
'''

# cur3 = conn.cursor()
# cur3.execute("SELECT auth_user.id,auth_user.username,newsapp_userprofile.nickname,newsapp_userprofile.birth,newsapp_userprofile.sex,newsapp_userprofile.location,newsapp_userprofile.school,newsapp_userprofile.vocation,newsapp_userprofile.china,newsapp_userprofile.world,newsapp_userprofile.social,newsapp_userprofile.mil,newsapp_userprofile.sport,newsapp_userprofile.tech,newsapp_userprofile.economic,newsapp_userprofile.funny, newsapp_ticket.choice, newsapp_ticket.article_id,newsapp_userlog.last_time,newsapp_userlog.times,newsapp_userlog.like_keywords,newsapp_article.headline,newsapp_article.url,newsapp_article.tag,newsapp_article.keywords FROM  auth_user JOIN newsapp_userprofile ON auth_user.id = newsApp_userprofile.belong_to_id JOIN newsapp_userlog ON newsapp_userlog.belong_to_id = auth_user.id JOIN newsapp_ticket ON newsApp_ticket.voter_id = auth_user.id WHERE auth_user.is_superuser IS FALSE AND =newsapp_ticket.article_id = newsapp_userlog.article_id")
cur4=conn.cursor()
cur4.execute("SELECT * FROM auth_user,newsapp_userlog,newsapp_ticket WHERE auth_user.is_superuser IS FALSE AND auth_user.id = newsapp_ticket.voter_id AND auth_user.id = newsapp_userlog.belong_to_id ")

cur5 = conn.cursor()
cur5.execute("SELECT * FROM newsapp_userlog")
news_List = []
news_article_df = DataFrame(columns=['id','headline','content','date','views','like','dislike','recommend','tag','source','url','keywords','images1','images2','images3','images4','images5'])

userlog_df = DataFrame(columns=['id','url','article_id','start_time', 'end_time','last_time','times','belong_to_id','like_keywords'])

for r in cur1.fetchall():
    article_id = r[0]
    headline = r[1]
    content = r[2]
    date = r[3]
    views = r[4]
    like = r[5]
    dislike = r[6]
    recommend = r[7]
    tag = r[8]
    source = r[9]
    url = r[10]
    keywords = r[11]
    images1= r[12]
    images2= r[13]
    images3= r[14]
    images4= r[15]
    images5= r[16]
    news_article_df=news_article_df.append(Series([id,headline,content,date,views,like,dislike,recommend,tag,source,url,keywords,images1,images2,images3,images4,images5],index=['id','headline','content','date','views','like','dislike','recommend','tag','source','url','keywords','images1','images2','images3','images4','images5']), ignore_index=True)

news_article_df.to_csv('D:\\news_article.csv',index=True,header=True)

#
# for v in cur2.fetchall():
#     print(v)
# #
# for v in cur3.fetchall():
#     print(v)
for v in cur4.fetchall():
    print(v)
for v in cur5.fetchall():
    print(v)
cur1.close()
# cur2.close()
# cur3.close()
cur4.close()
cur5.close()
conn.close()