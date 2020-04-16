from django.contrib import admin
from core.models import FakeTweet, RealTweet

admin.site.register(FakeTweet)
admin.site.register(RealTweet)
