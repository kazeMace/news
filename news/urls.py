"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from newsApp.views import index, detail, detail_comment,index_login, index_register, myinfo, mycollection, vote, cancel_collection, userlog,search
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from newsApp.api import article
from newsApp.newviews import newindex
from rest_framework.authtoken import views
# from django.conf.urls import url
# from haystack.views import SearchView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', index, name='index'),
    url(r'^newindex/$', newindex, name='newindex'),
    url(r'^userlog/(?P<username>[A-Za-z]+)/(?P<page_num>\d+)$', userlog, name='userlog'),

    # url(r'^detail/$', detail, name='detail'),
    url(r'^index/(?P<cate>[A-Za-z]+)$', index, name='index'),
    url(r'^newindex/(?P<cate>[A-Za-z]+)$', newindex, name='newindex'),
    url(r'^detail/(?P<page_num>\d+)$', detail, name='detail'),
    url(r'^detail/(?P<page_num>\d+)/comment$', detail_comment, name='comment'),
    url(r'^register/$', index_register, name="register"),
    url(r'^login/$', index_login, name="login"),
    url(r'^logout/', logout, {'next_page': '/index'}, name="logout"),
    url(r'^myinfo/(?P<username>[A-Za-z]+)$', myinfo, name="information"),
    url(r'^mycollection/(?P<username>[A-Za-z]+)$', mycollection, name="collection"),
    url(r'^vote/(?P<page_num>\d+)/$', vote, name="vote"),
    url(r'^cancel_collection/(?P<username>[A-Za-z]+)/(?P<page_num>\d+)/$', cancel_collection, name="cancel_collection"),



    url(r'^api/article/$', article, name="article_api"),
    # url(r'^search/$', SearchView(), name='haystack_search'),
    # (r'^search/', include('haystack.urls')),
    url(r'^search/$',search, name='search')
    # url(r'^search/(?P<cate>[A-Za-z]+)$',search, name='search')



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
