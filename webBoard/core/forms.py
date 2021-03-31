from django import forms
from django.forms import ModelForm
from webBoard.core.models import Topic

class create_topic_form(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
   # title = forms.CharField(max_length=50)
    #content = forms.CharField(max_length=150)

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']