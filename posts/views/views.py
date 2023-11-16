from collections import OrderedDict
from math import ceil

from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from posts import models as posts_models
from rest_framework.pagination import PageNumberPagination

from posts.serializers.post_rate_serializer import PostRateSerializer
from posts.serializers.post_serializer import PostSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("page_count", ceil(self.page.paginator.count / self.page_size)),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


# Create your views here.
class PostsView(ListCreateAPIView):
    queryset = posts_models.Post.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = PostSerializer


class PostRateView(CreateAPIView):
    serializer_class = PostRateSerializer

