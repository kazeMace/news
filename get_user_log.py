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

user_curs = conn.cursor()
user_curs.execute("SELECT auth_user.id, auth_user.username FROM auth_user")

# userprofile = DataFrame(column=['username'])
user_id_list = []
user_name_list = []
for user in user_curs.fetchall():
    user_id=user[0]
    # print(type(user_id))
    username=user[1]
    user_id_list.append(user_id)
    user_name_list.append(username)

# print(user_id_list)
# print(user_name_list)


sql = "SELECT auth_user.username, newsapp_userlog.article_id, newsapp_userlog.last_time, newsapp_userlog.times, newsapp_userlog.time, auth_user.id FROM newsapp_userlog, auth_user WHERE auth_user.is_superuser IS FALSE AND auth_user.id = newsapp_userlog.belong_to_id AND auth_user.id={}"
for user_id in user_id_list:
    userlog_curs = conn.cursor()
    print(user_id)
    new_sql = sql.format(str(user_id))
    print(new_sql)
    userlog_curs.execute(new_sql)


    for a in userlog_curs.fetchall():
        # print(a)
        username = a[0]
        article_id = a[1]
        last_time = a[2]
        times = a[3]
        date_time = a[4].strftime("%Y-%m-%d")
        user_id = a[5]
        print(username)
        # print(type(username))
        print(article_id)
        print(last_time)
        print(date_time)
        # print(type(date_time))
        userlog = DataFrame(columns=['user_id', 'username', 'article_id', 'last_time', 'times', 'date_time'])
        userlog = userlog.append(Series([user_id, username, article_id, last_time, times, date_time], index=['user_id', 'username','article_id','last_time','times','date_time']),ignore_index=True)

        print(userlog)

        userlog.to_csv("userlog_%s_%s.csv"%(user_id, date_time), index=True, header=True)
        print("**"*30)
    # username = a