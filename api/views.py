import json

from django.http import HttpResponse

from .models import Post, PostSerializer
from .utils import Utils


def home(request, *args, **kwargs):
    serializer = PostSerializer(Post.objects.all(), many=True)
    return HttpResponse(json.dumps(serializer.data), content_type="application/json")


def get_latest(request):
    utils = Utils()
    utils.scrap_hn()
    return HttpResponse("Posts retrieved.")