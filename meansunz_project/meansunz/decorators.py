from functools import wraps
import json

from django.http import HttpResponse


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        jsonr = json.dumps({'not_authenticated': True})
        return HttpResponse(jsonr, content_type='application/json')

    return wrapper
