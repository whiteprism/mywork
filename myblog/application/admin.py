from django.contrib import admin
from models import *
# Register your models here.

class blogPostAdmin(admin.ModelAdmin):
    list_display = ('title','content','time')

admin.site.register(blogPost,blogPostAdmin)
