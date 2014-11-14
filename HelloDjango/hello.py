import sys
import os

from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse


settings.configure(
    DEBUG=True,
    SECRET_KEY='GetYourOwn',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    STATIC_URL = '/static/',
    #STATIC_ROOT = os.path.join(BASE_DIR, '../static'),
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)


from django.conf.urls import url
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World!')


urlpatterns = (
    url(r'^$', index),
)


application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
