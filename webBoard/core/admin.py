from django.contrib import admin
from webBoard.core.models import *
# Register your models here.

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Create)
admin.site.register(Write)
admin.site.register(Tag)