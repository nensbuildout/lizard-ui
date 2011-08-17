import logging

from django.conf import settings

import lizard_ui.testsettings as example_settings

_checkers = []
logger = logging.getLogger(__name__)


def register(checker):
    """Register the checker function for the configchecker management command.

    Use this as a decorator:

        >>> from lizard_ui import configchecker
        >>> configchecker._checkers = []  # Only for Test initialization!
        >>> @configchecker.register
        ... def my_checker():
        ...     print "I'm checkin'"

    Warning: if you put the checker in a separate file, make sure that the
    file is actually imported, otherwise it isn't registered.

    The decorator registers the function so that the management command can
    run all those checker functions.

        >>> len(configchecker.checkers())
        1
        >>> configchecker.checkers()[0]()
        I'm checkin'

    """
    _checkers.append(checker)


def checkers():
    """Return registered checker functions."""
    return _checkers


@register
def checker():
    """Verify lizard_ui's demands on settings.py."""
    for setting in ['MEDIA_URL',
                    'STATIC_URL',
                    'ADMIN_MEDIA_PREFIX',
                    'MEDIA_ROOT',
                    'STATIC_ROOT',
                    'LOGGING',
                    'STATICFILES_FINDERS']:
        if not hasattr(settings, setting):
            logger.error("Setting %s is missing. Example value: %s",
                         setting, getattr(example_settings, setting))

    for app in ['lizard_ui',
                'compressor',
                'staticfiles',
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites']:
        if app not in settings.INSTALLED_APPS:
            logger.error("%s is missing from INSTALLED_APPS.", app)

