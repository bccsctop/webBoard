from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from webBoard.core.forms import *
from webBoard.core.models import *
import datetime

# Create your views here.
def home(request):
    count = User.objects.count()
    topic_all = Topic.objects.all()
    comment_all = Comment.objects.all()
    return render(request, 'home.html', {
        'count': count,'topic_all': topic_all , 'comment_all' : comment_all,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

def create_topic(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        form = create_topic_form(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            create_title = request.POST.get('title')
            create_content = request.POST.get('content')

            topic.title = create_title
            topic.content = create_content
            topic.user_name = request.user
            topic.like = 0
            topic.save()

            #time create topic
            create_time_topic = Create.objects.create(userid=request.user,
                                                        topicid=topic,
                                                        date=datetime.datetime.now())
        return HttpResponseRedirect("/")
    else:
        form = create_topic_form()
        return render(request, 'create_topic.html', {
        'form': form
    })

def create_comment(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        tpid = Topic.objects.get(topicid= topic_id)
        form = create_comment_form(request.POST)

        if form.is_valid():
            create_comment = request.POST.get('content')
            comment = form.save(commit=False)
            comment.comuserid = request.user
            comment.comtopicid = tpid
            comment.content = create_comment
            comment.like = 0
            comment.date = datetime.datetime.now()
            comment.save()

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)
    else:
        form = create_comment_form()
        return render(request, 'view_topic.html', {
        'form': form , 'select_topic' : select_topic
    })

def view_topic(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)

    comment_topic = Comment.objects.filter(comtopicid=topic_id)

    time_create_topic = Create.objects.get(userid=select_topic.user_name,topicid=select_topic)

    print(time_create_topic)

    return render(request, 'view_topic.html', { 'select_topic' : select_topic, 'comment_topic' : comment_topic, 
    'time_create_topic':time_create_topic})

def edit_topic(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        form = edit_topic_form(request.POST)
        if form.is_valid():
            edit_title = request.POST.get('title')
            edit_content = request.POST.get('content')
            
            edit_topic = Topic.objects.filter(topicid=topic_id).update(title=edit_title, content=edit_content)

        url_redirect = '/topic/' + str(select_topic.topicid)
        return HttpResponseRedirect(url_redirect)
    else:
        form = edit_topic_form()
        return render(request, 'edit_topic.html', {'form' : form, 'select_topic' : select_topic})

def delete_topic(request, topic_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    else:
        delete_topic = Topic.objects.filter(topicid=topic_id).delete()
        delete_comment = Comment.objects.filter(comtopicid=topic_id).delete()

        return HttpResponseRedirect("/")

def edit_comment(request, comment_id):
    select_comment = Comment.objects.get(commentid=comment_id)
    get_id_topic = Comment.objects.get(commentid=comment_id)
    select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

    topic_id = select_topic.topicid
    select_topic = Topic.objects.get(topicid=topic_id)

    comment_topic = Comment.objects.filter(comtopicid=topic_id)

    time_create_topic = Create.objects.get(userid=select_topic.user_name,topicid=select_topic)

    if request.method == 'POST':
        edit_content = request.POST.get('content')
        edit_comment = Comment.objects.filter(commentid=comment_id).update(content=edit_content)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)

    
    return render(request, 'edit_comment.html', { 'select_topic' : select_topic, 
    'comment_topic' : comment_topic, 
    'select_comment' : select_comment, 'time_create_topic' : time_create_topic})

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    else:
        get_id_topic = Comment.objects.get(commentid=comment_id)
        select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

        topic_id = select_topic.topicid
        delete_comment = Comment.objects.filter(commentid=comment_id).delete()
        
        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)

    

