from django.db import models
# from faker import Factory
from django.contrib.auth.models import User
import csv

# Create your models here.


class Article(models.Model):
    # article_id = models.CharField(default=id,max_length=100)
    headline = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=False)
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    TAG_CHOICE = (
        ('国内', '国内'),
        ('国际', '国际'),
        ('社会', '社会'),
        ('体育', '体育'),
        ('财经', '财经'),
        ('军事', '军事'),
        ('科技', '科技'),
        ('搞笑', '搞笑'),
    )
    recommend = models.BooleanField(default=False)
    tag = models.CharField(null=True, blank=True, max_length=10, choices=TAG_CHOICE)
    source = models.CharField(null=True, blank=True, max_length=50)
    url = models.CharField(null=True, blank=True, max_length=1000)
    keywords = models.CharField(null=True, blank=True, max_length=100)
    image1 = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    image3 = models.ImageField(null=True,blank=True)
    image4 = models.ImageField(null=True,blank=True)
    image5 = models.ImageField(null=True,blank=True)

    def __str__(self):

        return self.headline

class Recommend_Article(models.Model):
    belong_to = models.ForeignKey(to=User, related_name='user_name')
    article_id = models.CharField(null=True,blank=True, max_length=100)
    headline = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=False)
    TAG_CHOICE = (
        ('国内', '国内'),
        ('国际', '国际'),
        ('社会', '社会'),
        ('体育', '体育'),
        ('财经', '财经'),
        ('军事', '军事'),
        ('科技', '科技'),
        ('搞笑', '搞笑'),
    )
    recommend = models.BooleanField(default=False)
    tag = models.CharField(null=True, blank=True, max_length=10, choices=TAG_CHOICE)
    source = models.CharField(null=True, blank=True, max_length=50)
    keywords = models.CharField(null=True, blank=True, max_length=100)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

# fake = Factory.create()
# for i in range(0, 200):
#     v = Article(
#         headline=fake.text(max_nb_chars=90),
#         content=fake.text(max_nb_chars=3000),
#         # url_image=url,
#         # editors_choice=fake.pybool()
#         )
#     v.save()






class UserProfile(models.Model):

    # 关联到User的model
    belong_to = models.OneToOneField(to=User, related_name='profile', null=True, blank=True)

    # 用户姓名
    nickname = models.CharField(null=True, blank=True, max_length=14)

    # 用户生日
    birth = models.DateField(auto_now=False,null=True, blank=True)

    # 用户头像
    avatar = models.ImageField(upload_to='avatar')

    # 用户性别
    SEX_TAG = (
        ('男', '男'),
        ('女', '女'),
    )
    sex = models.CharField(null=True, blank=True, max_length=10, choices=SEX_TAG, default=None)

    # 用户邮箱
    email = models.EmailField(null=True)

    # 用户描述信息
    desc = models.CharField(null=True, blank=True, max_length=250)

    location = models.CharField(null=True, blank=True, max_length=50)

    school = models.CharField(null=True, blank=True, max_length=50)

    vocation = models.CharField(null=True, blank=True, max_length=50)

    # 用户兴趣
    china = models.BooleanField(default=False)
    world = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    mil = models.BooleanField(default=False)
    sport = models.BooleanField(default=False)
    tech = models.BooleanField(default=False)
    economic = models.BooleanField(default=False)
    funny = models.BooleanField(default=False)
    background_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.belong_to)


class Comment(models.Model):
    name = models.ForeignKey(to=UserProfile, related_name='comment_username', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    time = models.DateField(auto_now=True)
    belong_to = models.ForeignKey(to=Article, related_name='under_comments', null=True, blank=True)
    best_comment = models.BooleanField(default=False)
    like_count = models.ImageField(null=True, blank=True)
    dislike_count = models.ImageField(null=True, blank=True)
    def __str__(self):
        return str(self.id)


class Ticket(models.Model):
    voter = models.ForeignKey(to=User, related_name="user_tickets")
    article = models.ForeignKey(to=Article, related_name="article_tickets")

    ARTICLE_CHOICES = {
        ("like", "like"),
        ("dislike", "dislike"),
        ("normal", "normal")
    }
    choice = models.CharField(choices=ARTICLE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)



class Userlog(models.Model):
    belong_to = models.ForeignKey(to=User, related_name='user')
    url = models.URLField(max_length=200, null=True, blank=True)
    article_id = models.CharField(max_length=50, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True, auto_now=True)
    date = models.DateField(null=True, blank=True, auto_now=True)
    # end_time = models.DateTimeField(null=True, blank=True, auto_now=False)
    last_time = models.IntegerField(null=True, blank=True, default=0)
    times = models.IntegerField(default=0)
    like_keywords = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return str(self.id)


class Feedback(models.Model):
    belong_to = models.ForeignKey(to=User, related_name='feedback_user')
    feedback_content = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return str(self.id)


class banner_Article(models.Model):
    belong_to_article = models.OneToOneField(to=Article, related_name='banner', default=None)
    # headline = models.CharField(null=True, blank=True, max_length=300)
    # content = models.TextField(null=True, blank=True)
    # date = models.DateField(auto_now=False)
    # views = models.IntegerField(default=0)
    # like = models.IntegerField(default=0)
    # dislike = models.IntegerField(default=0)
    # TAG_CHOICE = (
    #     ('国内', '国内'),
    #     ('国际', '国际'),
    #     ('社会', '社会'),
    #     ('体育', '体育'),
    #     ('财经', '财经'),
    #     ('军事', '军事'),
    #     ('科技', '科技'),
    #     ('搞笑', '搞笑'),
    # )
    # recommend = models.BooleanField(default=False)
    # tag = models.CharField(null=True, blank=True, max_length=10, choices=TAG_CHOICE)
    # source = models.CharField(null=True, blank=True, max_length=50)
    # url = models.CharField(null=True, blank=True, max_length=1000)
    # keywords = models.CharField(null=True, blank=True, max_length=100)
    # image1 = models.ImageField(null=True, blank=True)
    # image2 = models.ImageField(null=True, blank=True)
    # image3 = models.ImageField(null=True, blank=True)
    # image4 = models.ImageField(null=True, blank=True)
    # image5 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.str

class hot_Article(models.Model):
    belong_to_article = models.OneToOneField(to=Article, related_name='hot_news', default=None)
    def __str__(self):
        return self.id

