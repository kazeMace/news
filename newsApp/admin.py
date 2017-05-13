from django.contrib import admin
from newsApp.models import Article, Comment, UserProfile, Ticket, Userlog, Recommend_Article
# Register your models here.


admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Ticket)
admin.site.register(Userlog)
admin.site.register(Recommend_Article)
# admin.site.register()
