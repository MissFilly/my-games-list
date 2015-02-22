import json
from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from mygameslist.app.models import ListEntry


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class EntryMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        self.entry = get_object_or_404(ListEntry, game__gamesdb_id=kwargs['slug'],
                                       user=request.user)
        return super(EntryMixin, self).dispatch(request, *args,
                                                **kwargs)


class PermissionMixin(LoginRequiredMixin, SingleObjectMixin):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        owner = None
        if hasattr(obj, 'user'):
            owner = obj.user
        elif hasattr(obj, 'entry'):
            owner = obj.entry.user
        elif hasattr(obj, 'entry1'):
            owner = obj.entry1.user
        elif hasattr(obj, 'to_user'):
            owner = obj.to_user

        if not owner == self.request.user:
            raise PermissionDenied()

        return obj


class JSONResponseMixin(object):

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context, default=lambda o: o.__dict__)
