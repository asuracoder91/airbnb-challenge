from django.contrib import admin
from .models import Tweet, Like


class ElonFilter(admin.SimpleListFilter):

    title = "Filter by like count"

    parameter_name = "likes"

    def lookups(self, request, model_admin):
        return [
            ("elon", "Tweets with Elon"),
            ("no_elon", "Tweets without Elon"),
        ]

    def queryset(self, request, tweets):
        likes = self.value()
        if likes == "elon":
            return tweets.filter(payload__contains='Elon Musk')
        elif likes == "no_elon":
            return tweets.exclude(payload__contains='Elon Musk')


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):

    list_display = (
        "payload",
        "user",
        "like_count",
    )

    search_fields = (
      "payload",
      "user__username",
    )

    list_filter = (
      ElonFilter,
      "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    search_fields = ("user__username", )

    list_filter = ("created_at", )
