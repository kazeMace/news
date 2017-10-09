from django.shortcuts import render, redirect, HttpResponse
from newsApp.models import Article, Comment, UserProfile, Ticket, Userlog,Recommend_Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newsApp.form import CommentForm, UserInfoForm, shijianform
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request, cate=None):
    print(request.user, type(request.user))
    print(request.user.username, type(request.user.username))
    if request.user.is_authenticated:
        user = request.user
        user_id = request.user.id
        print(user_id)
        if cate == 'china':
            article_list = Article.objects.filter(tag='国内')

        elif cate == 'world':
            article_list = Article.objects.filter(tag='国际')

        elif cate == 'social':
            article_list = Article.objects.filter(tag='社会')

        elif cate == 'sports':
            article_list = Article.objects.filter(tag='体育')

        elif cate == 'economic':
            article_list = Article.objects.filter(tag='财经')

        elif cate == 'mil':
            article_list = Article.objects.filter(tag='军事')

        elif cate == 'tech':
            article_list = Article.objects.filter(tag='科技')

        elif cate == 'funny':
            article_list = Article.objects.filter(tag='搞笑')

        elif cate == 'recommend':
            article_list = Recommend_Article.objects.filter(belong_to=user)
        else:
            # article_list = Article.objects.all()
            article_list = Recommend_Article.objects.filter(belong_to=user)
        if cate is None:
            article_list = Recommend_Article.objects.filter(belong_to=user)
        page_robot = Paginator(article_list, 6)
        page_num = request.GET.get('page')
    else:
        if cate == 'china':
            article_list = Article.objects.filter(tag='国内')

        elif cate == 'world':
            article_list = Article.objects.filter(tag='国际')

        elif cate == 'social':
            article_list = Article.objects.filter(tag='社会')

        elif cate == 'sports':
            article_list = Article.objects.filter(tag='体育')

        elif cate == 'economic':
            article_list = Article.objects.filter(tag='财经')

        elif cate == 'mil':
            article_list = Article.objects.filter(tag='军事')

        elif cate == 'tech':
            article_list = Article.objects.filter(tag='科技')

        elif cate == 'funny':
            article_list = Article.objects.filter(tag='搞笑')
        elif cate == 'recommend':
            article_list = Article.objects.order_by('-views')

        # else:
        #     article_list = Article.objects.order_by('-views')

        if cate is None:
            article_list = Article.objects.order_by('-views')
        page_robot = Paginator(article_list, 6)
        page_num = request.GET.get('page')
    try:

        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)
    if request.user.is_authenticated:

        login_user = request.user
        context = {}

        context['login_user'] = login_user
        context['article_list'] = article_list
        # context['recommend_article_list'] = recommend_article_list
        hot_article_list = Article.objects.order_by('-views')[0:5]
        context["hot_article_list"] = hot_article_list
        return render(request, 'index.html', context)
    else:
        context = {}
        context['article_list'] = article_list
        # context['recommend_article_list'] = recommend_article_list
        hot_article_list = Article.objects.order_by('-views')[0:5]
        context["hot_article_list"] = hot_article_list
        return render(request, 'index.html', context)


def detail(request, page_num, error_form=None):
    context = {}

    a = Article.objects.get(id=page_num)
    # 修改models的方法

    best_comment = Comment.objects.filter(best_comment=True, belong_to=a)
    if best_comment:
        context['best_comment'] = best_comment[0]
    if request.user.is_authenticated:
        a.views += 1
        a.save()
        # print(request.POST[])
        login_user = request.user
        context['login_user'] = login_user
        form = CommentForm

        article = Article.objects.get(id=page_num)
        url = request.path
        print(url)
        print(request.path_info)
        # print(tjArr)
        # userlog = Userlog(belong_to=login_user, url=url, article_id=page_num, times=1)
        # userlog.save()
        times = 0
        haslog = Userlog.objects.filter(belong_to=login_user, url=url, article_id=page_num)
        print("haslog:")
        print(haslog)
        try:
            if len(haslog)!=0 :
                thisuserlog = Userlog.objects.get(belong_to=login_user, url=url, article_id=page_num)
                times = thisuserlog.times
                now_last_time = thisuserlog.last_time
                thisuserlog.delete()
                userlog = Userlog(belong_to=login_user, url=url, article_id=page_num, last_time=now_last_time, times=times+1)
                userlog.save()
                print(times)
                print("has update")
            else:
                userlog = Userlog(belong_to=login_user, url=url, article_id=page_num, times=1)
                userlog.save()
        except:
            pass

        context['article'] = article
        # best_comment = Comment.objects.filter(best_comment=True, belong_to=article)
        # if best_comment:
        #     context['best_comment'] = best_comment[0]
        #     print(best_comment[0])

        if error_form is not None:
            context['form'] = error_form
        else:
            # 创建表单
            context['form'] = form
        try:
            user_voted = Ticket.objects.get(voter_id=request.user.id, article_id=page_num)
            context['user_voted'] = user_voted

        except:
            pass
        detail_page = render(request, 'detail.html', context)
        return HttpResponse(detail_page)
    else:
        form = CommentForm
        article = Article.objects.get(id=page_num)

        context['article'] = article

        if error_form is not None:
            context['form'] = error_form
        else:
            # 创建表单
            context['form'] = form
        try:

            user_voted = Ticket.objects.get(voter_id=request.user.id, article_id=page_num)
            context['user_voted'] = user_voted
        except:
            pass
        detail_page = render(request, 'detail.html', context)
        return HttpResponse(detail_page)


def detail_comment(request, page_num):
    if request.user.is_authenticated:
        login_user = request.user
        user_login = UserProfile.objects.get(belong_to=login_user)
        print(login_user)
        print(type(user_login))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            try:
                username = login_user.profile.nickname
            except:
                username = login_user.username
            article = Article.objects.get(id=page_num)
            c = Comment(name=user_login, comment=comment, belong_to=article)
            c.save()
        else:
            print(form.errors)
            return detail(request, page_num, error_form=form)

        return redirect(to='detail', page_num=page_num)
    else:
        return redirect(to='login')

def index_login(request):
    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            login_user = User.objects.get(username=username)
            if UserProfile.objects.filter(belong_to=login_user):
                pass
            else:
                new_userprofile = UserProfile(nickname=username, belong_to=login_user)
                new_userprofile.save()
            login(request, form.get_user())
            return redirect(to="index")


    context = {}
    context['form'] = form

    return render(request, 'login.html', context)


def index_register(request):
    if request.method == "GET":
        form = UserCreationForm
        print(User.username)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)


def myinfo(request, username):
    # 判断用户是否已经登录，如果没登录则返回登录界面

    if not isinstance(request.user, User):
        return redirect(to="login")
    now_user = User.objects.get(username=username)

    # 在user中查找是否有名称为username的用户，如果有，则进行下一步判断，如果没有，则返回主页
    try:
        check = User.objects.get(username=username)
        print(check)

    except:
        return redirect(to='index')
    if username == request.user.username:
        context = {}
        if request.method == 'GET':
            form = UserInfoForm
            # print(login_user.profile.nickname)
        if request.method == 'POST':
            form = UserInfoForm(request.POST, request.FILES)
            if form.is_valid():

                nickname = form.cleaned_data['修改昵称']
                avatar = form.cleaned_data['修改头像']
                birth = form.cleaned_data['生日']
                sex = form.cleaned_data['性别']
                email = form.cleaned_data['电子邮箱']
                desc = form.cleaned_data['个性签名']
                location = form.cleaned_data['所在地区']
                school = form.cleaned_data['毕业院校']
                vocation = form.cleaned_data['职业']
                interests = form.cleaned_data['兴趣']
                print(interests)
                china = 0
                world = 0
                social = 0
                mil = 0
                sport = 0
                tech = 0
                economic = 0
                funny = 0
                for type_index in interests:
                    if type_index == '国内':
                        china = 1
                    elif type_index == '国际':
                        world = 1
                    elif type_index == '社会':
                        social = 1
                    elif type_index == '军事':
                        mil = 1
                    elif type_index == '体育':
                        sport = 1
                    elif type_index == '科技':
                        tech = 1
                    elif type_index == '财经':
                        economic = 1
                    elif type_index == '搞笑':
                        funny = 1
                print(type(interests))
                change_userprofile = UserProfile(belong_to=now_user, nickname=nickname, birth=birth, avatar=avatar, sex=sex, email=email, desc=desc, location=location, school=school, vocation=vocation, china=china, world=world, social=social, mil=mil, sport=sport, tech=tech, economic=economic, funny=funny)
                # print(UserProfile.objects.get(belong_to=now_user))
                try:
                    if UserProfile.objects.get(belong_to=now_user):
                        now_nickname = UserProfile.objects.get(belong_to=now_user).nickname
                        pre_userprofile = UserProfile.objects.get(nickname=now_nickname)
                        pre_userprofile.delete()
                        change_userprofile.save()
                except:
                    change_userprofile.save()
                return redirect(to='information', username=username)
        try:
            login_user = UserProfile.objects.get(belong_to=now_user)
        except:
            login_user = now_user
        context['login_user'] = login_user
        context['form'] = form
        return render(request, 'information.html', context)
    else:
        return redirect(to='index')


def vote(request, page_num):
    # 未登录用户不允许投票，自动跳回详情页
    if not isinstance(request.user, User):
        return redirect(to="login")
    voter = request.user
    print(voter)
    voter_id = request.user.id
    print(voter_id)
    print(Ticket.objects.filter(voter_id=voter_id, article_id=page_num))


    if request.POST["vote"] == "like":
        has_voted = Ticket.objects.filter(voter_id=voter_id, article_id=page_num)
        if len(has_voted) == 0:
            new_ticket = Ticket(voter_id=voter_id, article_id=page_num, choice=request.POST["vote"])
            new_ticket.save()
            article = Article.objects.get(id=page_num)
            article.like += 1
            article.save()
        else:
            user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
            article = Article.objects.get(id=page_num)
            if user_ticket_for_this_article.choice == 'like':
                user_ticket_for_this_article.delete()
                article = Article.objects.get(id=page_num)
                article.like -= 1
                article.save()
            else:
                user_ticket_for_this_article.delete()
                article = Article.objects.get(id=page_num)
                article.dislike -= 1
                new_ticket = Ticket(voter_id=voter_id, article_id=page_num, choice=request.POST["vote"])
                new_ticket.save()

                article.like += 1
                article.save()

    if request.POST["vote"] == "dislike":
        has_voted = Ticket.objects.filter(voter_id=voter_id, article_id=page_num)
        if len(has_voted) == 0:
            new_ticket = Ticket(voter_id=voter_id, article_id=page_num, choice=request.POST["vote"])
            new_ticket.save()
            article = Article.objects.get(id=page_num)
            article.dislike += 1
            article.save()
        else:
            user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
            article = Article.objects.get(id=page_num)
            if user_ticket_for_this_article.choice == 'dislike':
                user_ticket_for_this_article.delete()
                article = Article.objects.get(id=page_num)
                article.dislike -= 1
                article.save()
            else:
                user_ticket_for_this_article.delete()
                article = Article.objects.get(id=page_num)
                article.like -= 1
                new_ticket = Ticket(voter_id=voter_id, article_id=page_num, choice=request.POST["vote"])
                new_ticket.save()

                article.dislike += 1
                article.save()

        # print(has_voted)
        # print(Ticket.objects.get(voter_id=voter_id,choice='dislike'))

    return redirect(to="detail", page_num=page_num)

def mycollection(request, username):
    if request.method == 'GET':
        # 未登录用户不允许收藏，自动跳回索引
        if not isinstance(request.user, User):
            return redirect(to='login')
        # print(request.user.username)
        # print(username)
        # print(request.user.id)
        #在注册用户中寻找登录名为username的用户，如果找到，则返回用户，否则返回首页
        try:
            login_user = User.objects.get(username=username)
            # print(login_user,type(login_user))
            # print(login_user.profile.nickname)
            # print(login_user.id)
            #
            # print(request.user, type(request.user))
            # print(request.user.profile.nickname)
        except:
            return redirect(to='index')
        #判断url中的用户名是否与已经登录的用户名一致，如果一致则进行下一步判断，否则返回首页
        if username == request.user.username:

            # print(type(login_user))
            # liker_id = request.user.id
            collection_list = Ticket.objects.filter(voter_id=login_user.id, choice='like')
            context = {}
            # login_user = UserProfile.objects.get(belong_to=now_user)
            context['login_user'] = login_user
            page_robot = Paginator(collection_list, 5)
            page_num = request.GET.get('page')
            try:
                collection_list = page_robot.page(page_num)
            except EmptyPage:
                collection_list = page_robot.page(page_robot.num_pages)
            except PageNotAnInteger:
                collection_list = page_robot.page(1)
            context['collection_list'] = collection_list
            return render(request, 'collection.html', context)
        else:
            return redirect(to='index')


def cancel_collection(request, username, page_num):
    # context = {}
    if request.method == 'POST':
        # if request.POST == 'cancel_collection':
        login_user = User.objects.get(username=username)
        article = Article.objects.get(id=page_num)
        collection = Ticket.objects.get(article=article,voter=login_user)
        # context['collection'] = collection
        # context['article'] = article
        collection.delete()
        article.like -= 1
        article.save()
        print(article.like)
        return redirect(to='collection', username=username)
'''
"url": "http://127.0.0.1:8000/detail/2", "time": 25, "refer": "http://127.0.0.1:8000/index/", "timeIn": 1493816722000, "timeOut": 1493816747000

'''


@csrf_exempt
def userlog(request, page_num, username):
    if request.method == 'POST':
        login_user = User.objects.get(username=username)
        article = Article.objects.get(id=page_num)
        log_list = []
        timelog = request.POST['timelog']
        timelog_split = timelog.split('},{')
        timelog_split.remove('[{')
        timelog_split[-1]=timelog_split[-1].split('}]')[0]
        new_time_log_list = timelog_split
        print('new_time_log_list::')
        print(new_time_log_list)
        new_time_log_lastly_str = new_time_log_list[-1]
        print('new_time_log_lastly_str::'+new_time_log_lastly_str)
        new_time_log_lastly_str_split_list = new_time_log_lastly_str.split(',')
        lastly_url = new_time_log_lastly_str_split_list[0].split('"')[-2]
        print(lastly_url)
        time_last = new_time_log_lastly_str_split_list[1].split(':')[1]
        print(time_last)
        last_article_id = lastly_url.split('/')[-1]
        if last_article_id == page_num:
            this_userlog = Userlog.objects.get(belong_to=login_user, article_id=page_num)
            now_last_time = this_userlog.last_time
            url = this_userlog.url
            times = this_userlog.times
            like_keywords = this_userlog.like_keywords
            print(now_last_time)
            new_last_time = int(time_last) + int(now_last_time)
            print('new_last_time:'+str(new_last_time))
            # this_userlog.last_time = int(new_last_time)
            this_userlog.delete()
            userlog = Userlog(belong_to=login_user, url=url ,article_id=last_article_id,times=times,like_keywords=like_keywords,last_time=int(new_last_time))
            userlog.save()

        return redirect(to='userlog', page_num=page_num, username=username)
        # pass


def search(request):
    if request.user.is_authenticated:
        login_user = request.user

        keyword = request.POST['searchWords']
        print(keyword)
        allArticle = Article.objects.all()
        SearchResult = []
        for x in allArticle:
            if keyword in x.headline:
                SearchResult.append(x)
            elif keyword in x.content:
                SearchResult.append(x)
        SearchStatus = "Error" if len(SearchResult) == 0 else "Success"
        ResultAmount = len(SearchResult)
        print(SearchResult)
        page_robot = Paginator(SearchResult, 6)
        page_num = request.GET.get('page')

        try:

            SearchResult = page_robot.page(page_num)
        except EmptyPage:
            SearchResult = page_robot.page(page_robot.num_pages)
        except PageNotAnInteger:
            SearchResult = page_robot.page(1)
        hot_article_list = Article.objects.order_by('-views')[0:5]

        return render(request, 'search.html', {"keyword": keyword,
                                                "SearchResult": SearchResult,
                                                "SearchStatus": SearchStatus,
                                                "ResultAmount": ResultAmount,
                                                'hot_article_list':hot_article_list,
                                                'login_user':login_user,
                                               })
    else:
        keyword = request.POST['searchWords']
        print(keyword)
        allArticle = Article.objects.all()
        SearchResult = []
        for x in allArticle:
            if keyword in x.headline:
                SearchResult.append(x)
            elif keyword in x.content:
                SearchResult.append(x)
        SearchStatus = "Error" if len(SearchResult) == 0 else "Success"
        ResultAmount = len(SearchResult)
        print(SearchResult)
        page_robot = Paginator(SearchResult, 6)
        page_num = request.GET.get('page')

        try:

            SearchResult = page_robot.page(page_num)
        except EmptyPage:
            SearchResult = page_robot.page(page_robot.num_pages)
        except PageNotAnInteger:
            SearchResult = page_robot.page(1)
        hot_article_list = Article.objects.order_by('-views')[0:5]

        return render(request, 'search.html', {"keyword": keyword,
                                               "SearchResult": SearchResult,
                                               "SearchStatus": SearchStatus,
                                               "ResultAmount": ResultAmount,
                                               'hot_article_list': hot_article_list,
                                               })



