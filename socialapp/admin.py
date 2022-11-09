from django.contrib import admin
from socialapp.models import Myuser, UserProfile, Posts, Comments
# Register your models here.
admin.site.register(Myuser)
admin.site.register(UserProfile)
admin.site.register(Posts)
admin.site.register(Comments)