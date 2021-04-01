from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from webBoard.core.forms import create_topic_form , create_comment_form
from webBoard.core.models import Topic

# Create your views here.
def home(request):
    count = User.objects.count()
    topic_all = Topic.objects.all()
    return render(request, 'home.html', {
        'count': count,'topic_all': topic_all
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
        #uname = request.user.username
        #print("Hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #print(uname)
        form = create_topic_form(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user_name = request.user

            topic.save()
        return HttpResponseRedirect("/")
    else:
        form = create_topic_form()
        return render(request, 'create_topic.html', {
        'form': form
    })

def create_comment(request):
    topic_id = request.GET.get('topicid')
    if not request.user.is_authenticated:
        return HttpResponseRedirect("accounts/login")
    elif request.method == 'POST':
        form = create_comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comuserid = request.user
            comment.like = 0
            comment.comtopicid = topic_id
            comment.save()
        return HttpResponseRedirect("/")
    else:
        form = create_comment_form()
        return render(request, 'create_comment.html', {
        'form': form , 'topic_id' : topic_id ,
    })