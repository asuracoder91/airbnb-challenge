from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TweetSerializer
from .models import Tweet
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework import status


class Tweets(APIView):
    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                tweet = serializer.save(
                    user=request.user,
                )
                serializer = TweetSerializer(tweet)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class OneTweet(APIView):
    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound("Tweet not found")

    def get(self, request, pk):
        tweet = self.get_object(pk=pk)
        serializer = TweetSerializer(
            tweet,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_object(pk=pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated("Tweet 수정을 위해서는 로그인해야합니다")
        if request.user != tweet.user:
            raise PermissionDenied("Tweet 작성자만 수정할 수 있습니다")
        serializer = TweetSerializer(
            tweet,
            data=request.data,
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        tweet = self.get_object(pk=pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated("Tweet 삭제를 위해서는 로그인해야합니다")
        if request.user != tweet.user:
            raise PermissionDenied("Tweet 작성자만 삭제할 수 있습니다")
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
