
import csv
import django
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
django.setup()
path ='C:/Users/张博航/我的桌面/news_item_info.csv'
import jieba.analyse
from newsApp.models import Article
with open(path, "r", encoding="utf-8") as csvfile:
    csvread = csv.reader(csvfile)
    for i in csvread:
        headline=i[0]
        date=i[1].split(' ')[0]
        content = i[2]
        url = i[3]
        tag = i[4]
        media_name = i[5]
        keywords = i[6]
        # print(keywords)
        # print(type(keywords))
        new_keywords =jieba.analyse.extract_tags(content,4)
        # print(new_keywords)
        # print(type(new_keywords))
        print(i)
        check = Article.objects.filter(headline=headline,date=date, content=content, url=url)
        if check:
            pass
        else:
            if keywords == 'None':
                print('XXXXXXXX')
                print(new_keywords)
                item = Article(
                    headline=headline,
                    date=date,
                    content=content,
                    tag=tag,
                    source=media_name,
                    url=url,
                    keywords=new_keywords,
                )
            elif keywords == '':
                print('IIIIIIIIII')
                print(new_keywords)
                item = Article(
                    headline=headline,
                    date=date,
                    content=content,
                    tag=tag,
                    source=media_name,
                    url=url,
                    keywords=new_keywords,
                )
            else:
                print("OOOOOOOOO")
                keywords_list = []
                print(keywords)

                for i in keywords.split(','):
                    # print(word)
                    keywords_list.append(i)
                print(keywords_list)
                item = Article(
                    headline=headline,
                    date=date,
                    content=content,
                    tag=tag,
                    source=media_name,
                    url=url,
                    keywords=keywords_list,
                )

        try:
            item.save()
        except:
            pass
