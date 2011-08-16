# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import View


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
        """Return response.

        In addition to what django's base template view does, we set ourselves
        (we're an object) as ``view`` in the context dictionary. This means
        that we can just set attributes on ourselves instead of assembling
        everything in a context dictionary. And the template can call methods
        that we provide. Handy!

        ``run()`` is called: do calculations in here.

        """
        self.context = {}
        self.context['view'] = self
        self.run()
        return self.render_to_response()

    def run(self):
        """Do calculations or so before rendering the response.

        Store attributes on self if you want to make them available in the
        template context. (Access them there as ``view.attribute``). Don't
        forget to call your superclass's run() method!

        """
        pass


class TestView(BaseView):
    template_name = 'lizard_ui/testview.html'
    bla = 0

    def method(self):
        self.bla += 1
        return self.bla

    def run(self):
        super(TestView, self).run()
        self.name = 'reinout'


class TestBox(BaseView):
    template_name = 'lizard_ui/testbox.html'

    def run(self):
        super(TestBox, self).run()
        self.name = self.kwargs['name']


class TestContainer(BaseView):
    template_name = 'lizard_ui/testcontainer.html'

    def box_urls(self):
        names = ['Reinout', 'Jack', 'Alexandr', 'Coen']
        urls = [reverse('lizard_ui.testbox',
                        kwargs={'name': name})
                for name in names]
        return urls

    def container_columns(self):
        columns = []
        column = {}
        column['id'] = 'column_1'
        column['class'] = 'one-third'
        column['box_urls'] = [
            reverse('lizard_ui.testbox',
                        kwargs={'name': 'reinout'}),
            ]
        columns.append(column)
        column = {}
        column['id'] = 'column_2'
        column['class'] = 'two-thirds'
        names = ['Jack', 'Alexandr', 'Coen']
        column['box_urls'] = [reverse('lizard_ui.testbox',
                                      kwargs={'name': name})
                              for name in names]
        columns.append(column)
        return columns

    def run(self):
        super(TestContainer, self).run()
