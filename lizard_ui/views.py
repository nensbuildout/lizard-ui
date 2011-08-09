# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin


def simple_login(request, next=None, template='lizard_ui/login.html'):
    """
    Logs a user in, replies success or failure in json success:
    {'success': success, 'next': next}

    If no username and password provided, you'll get a login screen.
    """
    post = request.POST
    if 'next' in post and post['next']:
        next = post['next']
        # print 'post next: %s' % next
    if 'next' in request.GET and request.GET['next']:
        next = request.GET['next']
        # print 'get next: %s' % next
    if 'username' not in post or 'password' not in post:
        return render_to_response(
            template,
            {'next': next},
            context_instance=RequestContext(request))
    username = post['username']
    password = post['password']
    user = authenticate(username=username, password=password)
    success = False
    if user is not None:
        if user.is_active:
            login(request, user)
            success = True
    return HttpResponse(json.dumps({'success': success, 'next': next}))


def simple_logout(request):
    """
    The simplest logout script possible, call this from a javascript using GET
    or POST.
    """
    logout(request)
    return HttpResponse("")


def example_breadcrumbs(request, template=None):
    crumbs = [{'name': 'name', 'url': 'url'},
              {'name': 'name2', 'url': 'url2'}]
    return render_to_response(
        template, {'crumbs': crumbs},
        context_instance=RequestContext(request))


def application_screen(
    request,
    application_screen_slug=None,
    template="lizard_ui/lizardbase.html",
    crumbs_prepend=None):
    """
    Render a screen with app icons. Not very useful, except for testing.
    """
    return render_to_response(
        template,
        {'application_screen_slug': application_screen_slug},
        context_instance=RequestContext(request))


class BaseView(View, TemplateResponseMixin):
    """Base class for lizard views, intended for subclassing.

    Lizard uses django's *class based views*. Our ``BaseView`` resembles
    django's ``TemplateView`` in that it implements the ``get()`` method and
    calls ``TemplateResponseMixin``'s ``render_to_response()``.

    Prerequisites for subclasses of BaseView:

    - Add a ``template_name`` attribute to your subclass (or implement
      ``get_template_names()`` from ``TemplateResponseMixin``). Alternatively,
      pass template_name as keyword argument in the ``urls.py`` call:
      ``.as_view(template_name=...)``.

    - Implement a ``run()`` method that does whatever you need to do and that
      fills the ``self.context`` dictionary with context items for the
      template.

    When returning something else apart from a template, you can overwrite
    ``render_to_response()`` to return something else, like a PNG picture.

    Several attributes are available:

    - ``self.request``: the request object.

    - ``self.args`` and ``self.kwargs``: the arguments from ``urls.py``.

    - ``self.context``: dictionary that gets passed as context to the
      template.

    TODO: perhaps factor most functionality out into a mixin class? [Reinout]

    """

    def render_to_response(self, **response_kwargs):
        """Render and return the response.

        Call TemplateResponseMixin's render_to_response with self.context
        instead of having to pass in the context by hand. Such a
        ``self.context`` attribute is much handier than passing it along from
        method to method.

        """
        return TemplateResponseMixin.render_to_response(
            self, self.context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        self.context = {}
        self.context['params'] = self.kwargs
        # ^^^ Django's TemplateView does this too.
        self.run()
        return self.render_to_response()

    def run(self):
        raise NotImplementedError


class TestView(BaseView):
    template_name = 'lizard_ui/testview.html'

    def run(self):
        self.context['name'] = 'reinout'
