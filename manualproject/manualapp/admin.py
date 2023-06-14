from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Step)
admin.site.register(Document)
admin.site.register(Bookmark)
