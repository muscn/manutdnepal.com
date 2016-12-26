from rest_framework import viewsets

from apps.key.permissions import DistributedKeyAuthentication
from apps.post.models import Post
from apps.post.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status='Published')
    permission_classes = (DistributedKeyAuthentication,)
