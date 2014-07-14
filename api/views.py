import datetime
import json
from django.http import HttpResponse

from api.utils import Utils


def home(request, *args, **kwargs):
    utils = Utils()
    posts = utils.get_posts()
    return HttpResponse(json.dumps(posts), content_type="application/json")
