INSTALLED_APPS = [
    'compressor',
    'staticfiles',
    'django_extensions',
    'django_nose',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    ]
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
    # Enable support for django-compressor.
    'compressor.finders.CompressorFinder',
    # Enable 'old' /media directories in addition to /static.
    'staticfiles.finders.LegacyAppDirectoriesFinder',
    )
