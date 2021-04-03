from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from webBoard.core.forms import create_topic_form , create_comment_form
from webBoard.core.models import *

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
        return HttpResponseRedirect("accounts/login")
    elif request.method == 'POST':
        form = create_topic_form(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user_name = request.user
            topic.like = 0
            topic.save()
        return HttpResponseRedirect("/")
    else:
        form = create_topic_form()
        return render(request, 'create_topic.html', {
        'form': form
    })

def create_comment(request):
    idtop = request.POST.get('fkid')
    select_topic = Topic.objects.get(topicid=idtop)

    if not request.user.is_authenticated:
        return HttpResponseRedirect("accounts/login")
    elif request.method == 'POST':
        idtop = request.POST.get('fkid')
        tpid = Topic.objects.get(topicid= idtop)
        form = create_comment_form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.comuserid = request.user
            comment.comtopicid = tpid
            comment.like = 0
            comment.save()

        url_redirect = '/topic/' + str(idtop)
        print(url_redirect)
        return HttpResponseRedirect(url_redirect)
    else:
        form = create_comment_form()
        return render(request, 'view_topic.html', {
        'form': form , 'select_topic' : select_topic
    })

def view_topic(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)
    form = create_comment_form()

    comment_topic = Comment.objects.filter(comtopicid=topic_id)
    return render(request, 'view_topic.html', { 'form': form , 'select_topic' : select_topic, 'comment_topic' : comment_topic})