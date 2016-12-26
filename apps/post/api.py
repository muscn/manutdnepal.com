from rest_framework import viewsets, mixins

from apps.key.permissions import DistributedKeyAuthentication
from apps.post.models import Post
from apps.post.serializers import PostSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status='Published')
    permission_classes = (DistributedKeyAuthentication,)
